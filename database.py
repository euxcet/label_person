import pymongo

class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['face']
        self.video_meta = self.db['video_meta']
        self.figure_meta = self.db['figure']
        self.score_col = self.db['score']
        # path times

    def search_video(self, video_path):
        for x in self.video_meta.find({'video_path': video_path}):
            return x
        return None

    def insert_video(self, video_path, output_path, frame_folder, face_folder):
        self.video_meta.insert_one({'video_path': video_path, 'output_path': output_path, 'frame_folder': frame_folder})

    def insert_figure(self, figure_path, face_path, times, x, y):
        self.figure_meta.insert_one({'path': figure_path, 'face': face_path, 'times': times, 'x': x, 'y': y})

    def clear(self):
        print(self.video_meta.delete_many({}).deleted_count)
        print(self.figure_meta.delete_many({}).deleted_count)
        print(self.score_col.delete_many({}).deleted_count)