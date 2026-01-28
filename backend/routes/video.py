from flask import Blueprint, jsonify, current_app
from models import Video
from middleware.jwt_auth import jwt_required, get_current_user_id
from utils.token_utils import generate_playback_token, verify_playback_token

video_bp = Blueprint('video', __name__)


def get_video_model():
    """Get Video model instance"""
    return Video(current_app.db)


@video_bp.route('/dashboard', methods=['GET'])
@jwt_required
def get_dashboard():
    """Get dashboard with 2 active videos (NO YouTube URLs exposed)"""
    user_id = get_current_user_id()
    current_app.logger.info(f"Dashboard accessed by user_id: {user_id}")
    
    video_model = get_video_model()
    videos = video_model.get_active_videos(limit=2)
    
    # Add playback token for each video
    for video in videos:
        video['playback_token'] = generate_playback_token(video['id'], user_id)
    
    return jsonify({
        'videos': videos
    }), 200


@video_bp.route('/video/<video_id>/stream', methods=['GET'])
@jwt_required
def get_video_stream(video_id):
    """
    Get video stream URL with token verification.
    Returns embed-safe YouTube URL only after verifying playback token.
    """
    from flask import request
    
    user_id = get_current_user_id()
    token = request.args.get('token')
    
    if not token:
        current_app.logger.warning(f"Missing playback token for video: {video_id} by user: {user_id}")
        return jsonify({'error': 'Playback token required'}), 400
    
    # Verify playback token
    if not verify_playback_token(token, video_id):
        current_app.logger.warning(f"Invalid playback token for video: {video_id} by user: {user_id}")
        return jsonify({'error': 'Invalid or expired playback token'}), 403
    
    # Get video details
    video_model = get_video_model()
    video = video_model.find_by_id(video_id)
    
    if not video:
        return jsonify({'error': 'Video not found'}), 404
    
    current_app.logger.info(f"Video stream authorized: {video_id} ('{video['title']}') for user: {user_id}")
    
    # Return embed-safe URL (YouTube embed format, not direct watch URL)
    embed_url = f"https://www.youtube.com/embed/{video['youtube_id']}?autoplay=1&controls=1"
    
    return jsonify({
        'video_id': video['id'],
        'title': video['title'],
        'stream_url': embed_url
    }), 200
