bl_info = {
    "name": "Mouse Tracker Import/Export",
    "author": "Dvir Marmor",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Clip Editor > Mouse Tracker I/O",
    "description": "Import, export, and process mouse tracking data",
    "warning": "",
    "doc_url": "",
    "category": "Motion Tracking",
}

import bpy
import csv
import os
from bpy.props import StringProperty, FloatProperty, EnumProperty
from bpy.types import Panel, Operator, PropertyGroup
from collections import defaultdict
import numpy as np

class TrackerProperties(PropertyGroup):
    input_csv: StringProperty(
        name="Input CSV",
        description="Path to input CSV file",
        default="",
        subtype='FILE_PATH'
    )
    input_mp4: StringProperty(
        name="Input MP4",
        description="Path to input MP4 file",
        default="",
        subtype='FILE_PATH'
    )
    processed_csv: StringProperty(
        name="Processed CSV",
        description="Path to processed CSV file",
        default="",
        subtype='FILE_PATH'
    )
    threshold: FloatProperty(
        name="Movement Threshold",
        description="Threshold for marker movement",
        default=50.0,
        min=0.0
    )
    def get_tracker_classes(self, context):
        clip = context.space_data.clip
        if clip:
            return [(track.name, track.name, "") for track in clip.tracking.objects["Camera"].tracks]
        return [("", "No clip loaded", "")]

    selected_tracker_class: EnumProperty(
        name="Select Tracker",
        description="Choose the tracker to reprocess",
        items=get_tracker_classes
    )

class CSVProcessor:
    @staticmethod
    def process_csv(input_csv, processed_csv, threshold):
        with open(input_csv, 'r') as infile:
            reader = csv.DictReader(infile)
            data = list(reader)

        # Group data by Frame, then by Class
        grouped_data = defaultdict(lambda: defaultdict(list))
        for row in data:
            frame = int(row['Frame'])
            class_id = int(row['Class'])
            grouped_data[frame][class_id].append((float(row['X']), float(row['Y'])))

        # Process data frame by frame
        processed_data = []
        for frame, frame_data in sorted(grouped_data.items()):
            for mouse_index in range(5):  # Assuming 5 mice
                body_class = mouse_index * 2
                head_class = mouse_index * 2 + 1

                body_points = frame_data.get(body_class, [])
                head_points = frame_data.get(head_class, [])

                # Handle body points
                if body_points:
                    if len(body_points) > 1:
                        # If multiple body points, choose the one closest to the head
                        if head_points:
                            head_point = head_points[0]  # Use the first head point as reference
                            body_point = min(body_points, key=lambda p: ((p[0]-head_point[0])**2 + (p[1]-head_point[1])**2)**0.5)
                        else:
                            body_point = body_points[0]  # If no head point, use the first body point
                    else:
                        body_point = body_points[0]

                    processed_data.append({
                        'Frame': frame,
                        'ID': f'Class_{body_class}',
                        'Class': body_class,
                        'X': body_point[0],
                        'Y': body_point[1]
                    })

                # Handle head points
                if head_points:
                    if len(head_points) > 1:
                        # If multiple head points, choose the one closest to the body
                        if body_points:
                            body_point = body_points[0]  # Use the first body point as reference
                            head_point = min(head_points, key=lambda p: ((p[0]-body_point[0])**2 + (p[1]-body_point[1])**2)**0.5)
                        else:
                            head_point = head_points[0]  # If no body point, use the first head point
                    else:
                        head_point = head_points[0]

                    processed_data.append({
                        'Frame': frame,
                        'ID': f'Class_{head_class}',
                        'Class': head_class,
                        'X': head_point[0],
                        'Y': head_point[1]
                    })

        # Sort processed data by Frame, then by Class
        processed_data.sort(key=lambda x: (x['Frame'], x['Class']))

        # Interpolate missing frames and apply threshold
        interpolated_data = CSVProcessor.interpolate_and_threshold(processed_data, threshold)

        # Write processed and interpolated data to CSV
        with open(processed_csv, 'w', newline='') as outfile:
            fieldnames = ['Frame', 'ID', 'Class', 'X', 'Y']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(interpolated_data)

    @staticmethod
    def interpolate_and_threshold(data, threshold):
        # Group data by Class
        grouped_data = defaultdict(list)
        for row in data:
            grouped_data[row['Class']].append(row)

        interpolated_data = []

        for class_id, class_data in grouped_data.items():
            frames = np.array([row['Frame'] for row in class_data])
            x_values = np.array([row['X'] for row in class_data])
            y_values = np.array([row['Y'] for row in class_data])

            # Create a full range of frames
            full_frames = np.arange(frames.min(), frames.max() + 1)

            # Interpolate X and Y values
            x_interp = np.interp(full_frames, frames, x_values)
            y_interp = np.interp(full_frames, frames, y_values)

            # Apply threshold to interpolated values
            prev_x, prev_y = x_interp[0], y_interp[0]
            for i, (frame, x, y) in enumerate(zip(full_frames, x_interp, y_interp)):
                if i > 0:
                    if abs(x - prev_x) > threshold or abs(y - prev_y) > threshold:
                        x, y = prev_x, prev_y
                interpolated_data.append({
                    'Frame': int(frame),
                    'ID': f'Class_{class_id}',
                    'Class': class_id,
                    'X': x,
                    'Y': y
                })
                prev_x, prev_y = x, y

        # Sort interpolated data by Frame, then by Class
        interpolated_data.sort(key=lambda x: (x['Frame'], x['Class']))
        return interpolated_data

class TRACKER_OT_import(Operator):
    bl_idname = "tracker.import"
    bl_label = "Import and Process Trackers"

    def execute(self, context):
        props = context.scene.tracker_props
        
        # Process the CSV file
        CSVProcessor.process_csv(props.input_csv, props.processed_csv, props.threshold)
        
        # Load the video into the Movie Clip Editor
        clip = bpy.data.movieclips.load(filepath=props.input_mp4)
        
        # Set the loaded clip as active in the Movie Clip Editor
        for area in bpy.context.screen.areas:
            if area.type == 'CLIP_EDITOR':
                area.spaces.active.clip = clip
                break

        # Set scene frame start and end to match the clip
        context.scene.frame_start = clip.frame_start
        context.scene.frame_end = clip.frame_start + clip.frame_duration - 1

        # Load tracking data from processed CSV
        self.load_tracking_data(clip, props.processed_csv)

        # Force Blender to update the view
        bpy.ops.clip.view_all()

        self.report({'INFO'}, f"Trackers imported and processed from {props.input_csv}")
        return {'FINISHED'}

    def load_tracking_data(self, clip, csv_path):
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            tracks = defaultdict(list)
            
            for row in reader:
                tracks[int(row['Class'])].append({
                    'frame': int(row['Frame']),
                    'x': float(row['X']),
                    'y': float(row['Y'])
                })

        for class_id, markers in tracks.items():
            track = clip.tracking.tracks.new(name=f"Class_{class_id}")
            for marker in markers:
                blender_marker = track.markers.insert_frame(marker['frame'])
                blender_marker.co = (marker['x'] / clip.size[0], 1 - (marker['y'] / clip.size[1]))

class TRACKER_OT_export(Operator):
    bl_idname = "tracker.export"
    bl_label = "Export Trackers"

    def execute(self, context):
        props = context.scene.tracker_props
        clip = context.space_data.clip

        if not clip:
            self.report({'ERROR'}, "No clip loaded in the Movie Clip Editor")
            return {'CANCELLED'}

        try:
            self.export_tracking_data(clip, props.processed_csv)
            self.report({'INFO'}, f"Trackers exported to {props.processed_csv}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error during export: {str(e)}")
            return {'CANCELLED'}

    def export_tracking_data(self, clip, csv_path):
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Frame', 'ID', 'Class', 'X', 'Y'])

            frame_start = clip.frame_start
            frame_end = frame_start + clip.frame_duration - 1

            print(f"Exporting frames from {frame_start} to {frame_end}")

            for track in clip.tracking.tracks:
                print(f"Processing track: {track.name}")
                try:
                    class_id = int(track.name.split('_')[1])
                except IndexError:
                    print(f"Warning: Unable to extract class ID from track name: {track.name}")
                    class_id = 0  # or some default value

                for frame in range(frame_start, frame_end + 1):
                    marker = track.markers.find_frame(frame)
                    
                    if marker and marker.mute == False:
                        # Convert normalized coordinates back to pixel coordinates
                        x = marker.co[0] * clip.size[0]
                        y = (1 - marker.co[1]) * clip.size[1]
                        
                        writer.writerow([frame, track.name, class_id, x, y])
                        print(f"Wrote data for frame {frame}, track {track.name}")
                    else:
                        print(f"No valid marker found for frame {frame}, track {track.name}")

            print("Export completed")

        # Check if any data was written
        with open(csv_path, 'r') as f:
            lines = f.readlines()
            if len(lines) <= 1:
                print("Warning: Only headers were written to the CSV file.")
            else:
                print(f"Successfully wrote {len(lines) - 1} data rows to the CSV file.")

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'CLIP_EDITOR' and context.space_data.clip

class TRACKER_OT_reprocess(Operator):
    bl_idname = "tracker.reprocess"
    bl_label = "Reprocess Track"

    def execute(self, context):
        props = context.scene.tracker_props
        clip = context.space_data.clip

        if not clip:
            self.report({'ERROR'}, "No clip loaded in the Movie Clip Editor")
            return {'CANCELLED'}

        class_name = props.selected_tracker_class
        if not class_name:
            self.report({'ERROR'}, "No tracker selected from the dropdown")
            return {'CANCELLED'}

        try:
            selected_track = clip.tracking.objects["Camera"].tracks[class_name]
        except KeyError:
            self.report({'ERROR'}, f"No track found for class {class_name}")
            return {'CANCELLED'}

        class_id = int(class_name.split('_')[1])
        current_frame = context.scene.frame_current
        fps = clip.fps

        # Reprocess from current frame to end
        self.reprocess_track(props.input_csv, props.processed_csv, class_id, current_frame, clip.frame_duration, fps, props.threshold)

        # Reload the clip with updated tracking data
        self.reload_clip_with_new_data(clip, props.input_mp4, props.processed_csv)

        self.report({'INFO'}, f"Reprocessed track {class_name} from frame {current_frame}")
        return {'FINISHED'}

    def reprocess_track(self, input_csv, processed_csv, selected_class_id, start_frame, total_frames, fps, threshold):
        # Determine the paired class ID (body if head, head if body)
        paired_class_id = selected_class_id - 1 if selected_class_id % 2 else selected_class_id + 1

        # Read all CSV data
        with open(input_csv, 'r') as file:
            reader = csv.DictReader(file)
            all_data = list(reader)

        # Group data by Frame, then by Class
        grouped_data = defaultdict(lambda: defaultdict(list))
        for row in all_data:
            frame = int(row['Frame'])
            class_id = int(row['Class'])
            if frame >= start_frame and class_id in (selected_class_id, paired_class_id):
                grouped_data[frame][class_id].append((float(row['X']), float(row['Y'])))

        # Process data frame by frame
        processed_data = []
        for frame, frame_data in sorted(grouped_data.items()):
            selected_points = frame_data.get(selected_class_id, [])
            paired_points = frame_data.get(paired_class_id, [])

            if selected_points:
                if len(selected_points) > 1 and paired_points:
                    # If multiple points, choose the one closest to the paired point
                    paired_point = paired_points[0]  # Use the first paired point as reference
                    selected_point = min(selected_points, key=lambda p: ((p[0]-paired_point[0])**2 + (p[1]-paired_point[1])**2)**0.5)
                else:
                    selected_point = selected_points[0]

                processed_data.append({
                    'Frame': frame,
                    'ID': f'Class_{selected_class_id}',
                    'Class': selected_class_id,
                    'X': selected_point[0],
                    'Y': selected_point[1]
                })

        # Sort the processed data
        processed_data.sort(key=lambda x: x['Frame'])

        # Apply threshold
        threshold_removed_until_frame = start_frame + fps
        prev_x, prev_y = None, None

        for row in processed_data:
            frame = int(row['Frame'])
            x, y = float(row['X']), float(row['Y'])

            if prev_x is not None and prev_y is not None:
                if frame >= threshold_removed_until_frame:
                    if abs(x - prev_x) > threshold or abs(y - prev_y) > threshold:
                        x, y = prev_x, prev_y

            row['X'], row['Y'] = str(x), str(y)
            prev_x, prev_y = x, y

        # Read existing processed CSV data
        with open(processed_csv, 'r') as file:
            reader = csv.DictReader(file)
            existing_data = [row for row in reader if int(row['Class']) != selected_class_id or int(row['Frame']) < start_frame]

        # Merge and write the data back to the processed CSV
        all_data = existing_data + processed_data
        all_data.sort(key=lambda x: (int(x['Frame']), int(x['Class'])))

        with open(processed_csv, 'w', newline='') as file:
            fieldnames = ['Frame', 'ID', 'Class', 'X', 'Y']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)

    def reload_clip_with_new_data(self, clip, video_path, csv_path):
        # Clear existing tracks
        bpy.ops.clip.select_all(action='SELECT')
        bpy.ops.clip.delete_track()

        # Reload the video clip
        bpy.data.movieclips.remove(clip)
        new_clip = bpy.data.movieclips.load(filepath=video_path)
        
        for area in bpy.context.screen.areas:
            if area.type == 'CLIP_EDITOR':
                area.spaces.active.clip = new_clip
                break

        # Load new tracking data
        self.load_tracking_data(new_clip, csv_path)

        # Update the view
        bpy.ops.clip.view_all()

    @staticmethod
    def load_tracking_data(clip, csv_path):
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            tracks = defaultdict(list)
            
            for row in reader:
                tracks[int(row['Class'])].append({
                    'frame': int(row['Frame']),
                    'x': float(row['X']),
                    'y': float(row['Y'])
                })

        for class_id, markers in tracks.items():
            track = clip.tracking.tracks.new(name=f"Class_{class_id}")
            for marker in markers:
                blender_marker = track.markers.insert_frame(marker['frame'])
                blender_marker.co = (marker['x'] / clip.size[0], 1 - (marker['y'] / clip.size[1]))

class TRACKER_PT_main_panel(Panel):
    bl_label = "Mouse Tracker Import/Export"
    bl_idname = "TRACKER_PT_main_panel"
    bl_space_type = 'CLIP_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Mouse Tracker I/O"

    def draw(self, context):
        layout = self.layout
        props = context.scene.tracker_props

        # Import section
        box = layout.box()
        box.label(text="Import and Process")
        box.prop(props, "input_csv")
        box.prop(props, "input_mp4")
        box.prop(props, "threshold")
        box.operator("tracker.import")

        # Export section
        box = layout.box()
        box.label(text="Export")
        box.prop(props, "processed_csv")
        box.operator("tracker.export")
        
        # Reprocess section
        box = layout.box()
        box.label(text="Reprocess Track")
        box.prop(props, "selected_tracker_class")
        box.operator("tracker.reprocess")

classes = (
    TrackerProperties,
    TRACKER_OT_import,
    TRACKER_OT_export,
    TRACKER_OT_reprocess,
    TRACKER_PT_main_panel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.tracker_props = bpy.props.PointerProperty(type=TrackerProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.tracker_props

if __name__ == "__main__":
    register()
