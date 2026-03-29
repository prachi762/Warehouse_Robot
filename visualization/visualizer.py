import os
import sys
import cv2

try:
    from PIL import Image, ImageDraw
except ImportError as ex:
    raise ImportError(
        "Pillow is not installed. Run `python -m pip install pillow` and rerun."
    ) from ex

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class WarehouseVisualizer:
    def __init__(self, grid, title="Search_Visualizer", cell_size=50):
        self.grid = grid
        self.cell_size = cell_size
        self.algorithm_name = title

        safe_title = title.replace(" ", "_").replace("*", "star")
        
        self.base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "outputs", safe_title)
        )
        self.dirs = {
            "grids": os.path.join(self.base_dir, "grids"),
            "paths": os.path.join(self.base_dir, "paths"),
            "frames": os.path.join(self.base_dir, "frames"),
        }
        for d in self.dirs.values():
            os.makedirs(d, exist_ok=True)

        self.canvas_w = self.grid.N * self.cell_size
        self.canvas_h = (self.grid.N * self.cell_size) + 60

        self.frame_count = 0

    def _make_pil_image(self, state=None, explored_keys=None, path_history=None):
        img = Image.new("RGB", (self.canvas_w, self.canvas_h), "white")
        draw = ImageDraw.Draw(img)

        for y in range(self.grid.N):
            for x in range(self.grid.N):
                x1 = x * self.cell_size
                y1 = y * self.cell_size + 60
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                fill = "white"

                if self.grid.grid[y][x] == 1:
                    fill = "#2d3436"  
                elif (x, y) == self.grid.delivery:
                    fill = "#e74c3c"  
                elif (x, y) == self.grid.start:
                    fill = "#3498db" 
s
                if explored_keys and (x, y) in {(k[0], k[1]) for k in explored_keys}:
                    if fill == "white":
                        fill = "#dfe6e9"  

                if path_history and (x, y) in path_history:
                    if fill in ["white", "#dfe6e9"]: 
                        fill = "#55efc4"  

                draw.rectangle([x1, y1, x2, y2], fill=fill, outline="#b2bec3")

        collected_mask = getattr(state, "collected", 0) if state else 0
        
        for (ix, iy), idx in getattr(self.grid, "item_map", {}).items():
            if not (collected_mask & (1 << idx)):
                cx = ix * self.cell_size + 25
                cy = iy * self.cell_size + 85
                draw.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill="#e67e22", outline="#d35400")

        if state is not None:
            rx = getattr(state, "x", 0) * self.cell_size + 10
            ry = getattr(state, "y", 0) * self.cell_size + 70
            
            draw.rectangle([rx, ry, rx + 30, ry + 30], fill="#2ecc71", outline="#27ae60")

            stats = (
                f"{self.algorithm_name} | Energy: {getattr(state, 'energy', 0)} "
                f"| Value: {getattr(state, 'value', 0)}"
            )
        else:
            stats = f"{self.algorithm_name} | Initial Grid"

        draw.text((10, 20), stats, fill="black")

        return img

    def save_canvas_as_image(self, category, filename, state=None, explored_keys=None, path_history=None):
        target_path = os.path.join(self.dirs[category], filename)
        img = self._make_pil_image(state=state, explored_keys=explored_keys, path_history=path_history)
        img.save(target_path, "PNG")
        img.close()

    def generate_ascii_view(self, state=None):
        ascii_lines = []
        ascii_lines.append("#" * (self.grid.N + 2))
        
        for y in range(self.grid.N):
            row_chars = ["#"]
            for x in range(self.grid.N):
                char = "."

                cell_value = self.grid.grid[y][x]
                if cell_value == 1:
                    char = "#"
                elif cell_value > 1:
                    char = str(cell_value)

                if (x, y) == self.grid.start:
                    char = "S"
                elif (x, y) == self.grid.delivery:
                    char = "D"

                collected_mask = getattr(state, "collected", 0) if state else 0
                for (ix, iy), idx in getattr(self.grid, "item_map", {}).items():
                    if (x, y) == (ix, iy):
                        if not state or not (collected_mask & (1 << idx)):
                            char = "I"

                if state and getattr(state, "x", -1) == x and getattr(state, "y", -1) == y:
                    char = "R"
                    
                row_chars.append(char)
                
            row_chars.append("#")
            ascii_lines.append("".join(row_chars))
            
        ascii_lines.append("#" * (self.grid.N + 2))
        return "\n".join(ascii_lines)

    def save_initial_grid(self):
        ascii_str = self.generate_ascii_view(state=None)
        
        target_path = os.path.join(self.dirs["grids"], "initial_grid.txt")
        with open(target_path, "w") as f:
            f.write(ascii_str)

    def save_path_frames(self, path_states, explored_keys_states=None):
        path_history = [] 
        
        for idx, state in enumerate(path_states):
            explored_keys = None
            if explored_keys_states:
                explored_keys = explored_keys_states[idx] if idx < len(explored_keys_states) else explored_keys_states[-1]
            
            path_history.append((getattr(state, "x", 0), getattr(state, "y", 0)))
            
            self.save_canvas_as_image(
                "frames", f"frame_{self.frame_count:04d}.png", 
                state=state, explored_keys=explored_keys, path_history=path_history
            )
            self.frame_count += 1

        if path_states:
            self.save_canvas_as_image(
                "paths", "final_path_result.png", 
                state=path_states[-1], explored_keys=explored_keys, path_history=path_history
            )

    def generate_mp4(self, fps=10, hold_end_seconds=3):
        frames_dir = self.dirs["frames"]
        
        safe_name = self.algorithm_name.replace(" ", "_").replace("*", "star")
        video_path = os.path.join(self.base_dir, f"{safe_name}_demo.mp4")

        images = [img for img in os.listdir(frames_dir) if img.endswith(".png")]
        images.sort()

        if not images:
            return

        first_frame_path = os.path.join(frames_dir, images[0])
        frame = cv2.imread(first_frame_path)
        height, width, layers = frame.shape

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

        for image in images:
            img_path = os.path.join(frames_dir, image)
            video.write(cv2.imread(img_path))

        last_frame_path = os.path.join(frames_dir, images[-1])
        last_frame = cv2.imread(last_frame_path)
        
        hold_frame_count = fps * hold_end_seconds
        for _ in range(hold_frame_count):
            video.write(last_frame)

        video.release()
        
        print(f"[{self.algorithm_name}] -> Video saved to: {safe_name}_demo.mp4")

    def save_final_results(self, path_states, explored_keys_states=None, delay=0.05):
        print(f"[{self.algorithm_name}] -> Generating frames in background...")
        self.save_initial_grid()
        self.save_path_frames(path_states, explored_keys_states=explored_keys_states)
        self.generate_mp4(fps=10)
