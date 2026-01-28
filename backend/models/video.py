from bson import ObjectId


class Video:
    """Video model for MongoDB"""
    
    def __init__(self, db):
        self.collection = db['videos']
    
    def get_active_videos(self, limit: int = 2) -> list:
        """Get active videos for dashboard"""
        videos = self.collection.find({'is_active': True}).limit(limit)
        return [self._serialize_for_dashboard(v) for v in videos]
    
    def find_by_id(self, video_id: str) -> dict | None:
        """Find video by ID (includes youtube_id for internal use)"""
        try:
            video = self.collection.find_one({'_id': ObjectId(video_id)})
            if video:
                return self._serialize_full(video)
        except Exception:
            pass
        return None
    
    def seed_videos(self):
        """Seed initial video data if collection is empty"""
        if self.collection.count_documents({}) == 0:
            videos = [
                {
                    'title': 'How Startups Fail',
                    'description': 'Lessons from real founders about common startup mistakes and how to avoid them.',
                    'youtube_id': 'dQw4w9WgXcQ',  # Example YouTube ID
                    'thumbnail_url': 'https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',
                    'is_active': True
                },
                {
                    'title': 'Building Great Products',
                    'description': 'Learn the fundamentals of product development from industry experts.',
                    'youtube_id': '9bZkp7q19f0',  # Example YouTube ID
                    'thumbnail_url': 'https://img.youtube.com/vi/9bZkp7q19f0/maxresdefault.jpg',
                    'is_active': True
                }
            ]
            self.collection.insert_many(videos)
            print("✓ Seeded 2 videos into database")
    
    def _serialize_for_dashboard(self, video: dict) -> dict:
        """Serialize video for dashboard (NO youtube_id exposed)"""
        return {
            'id': str(video['_id']),
            'title': video['title'],
            'description': video['description'],
            'thumbnail_url': video['thumbnail_url']
        }
    
    def _serialize_full(self, video: dict) -> dict:
        """Full serialization (internal use only)"""
        return {
            'id': str(video['_id']),
            'title': video['title'],
            'description': video['description'],
            'youtube_id': video['youtube_id'],
            'thumbnail_url': video['thumbnail_url'],
            'is_active': video['is_active']
        }
