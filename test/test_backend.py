from main.backend import Backend

def test_resolutions():
    backend = Backend(None)  # Pass None for window since we won't use it
    backend.video_data = [
        {'res': 720, 'vcodec_name': 'h264'},
        {'res': 1080, 'vcodec_name': 'h264'},
        {'res': 480, 'vcodec_name': 'vp9'},
        {'res': 360, 'vcodec_name': 'h264'},
        {'res': 27, 'vcodec_name': 'h264'},  
        {'res': 45, 'vcodec_name': 'h264'},  
        {'res': 90, 'vcodec_name': 'h264'},   
    ]
    
    fetched_res = backend.resolutions()
    
    expected_res = ['1080p', '720p', '480p', '360p']
    assert fetched_res == expected_res

def test_populate_resolutions_with_no_video_data():
    backend = Backend(None)
    backend.video_data = []
    
    fetched_res = backend.resolutions()
    
    assert fetched_res == []

def test_codec_for_resolution():
    backend = Backend(None)  # Pass None for window since we won't use it
    backend.video_data = [
        {'res': 720, 'vcodec_name': 'h264'},
        {'res': 720, 'vcodec_name': 'vp9'},  
        {'res': 720, 'vcodec_name': 'av01'},  
        {'res': 1080, 'vcodec_name': 'h264'},
        {'res': 1080, 'vcodec_name': 'vp9'},  
        {'res': 480, 'vcodec_name': 'vp9'},
        {'res': 360, 'vcodec_name': 'h264'},
    ]

    codecs = backend.codecs_for_resolution(720)
    expected_codecs = ['h264', 'vp9', 'av01']
    assert codecs == expected_codecs

def test_codec_for_resolution_with_no_matching_resolution():
    backend = Backend(None)
    backend.video_data = [
        {'res': 720, 'vcodec_name': 'h264'},
        {'res': 1080, 'vcodec_name': 'h264'},
    ]

    codecs = backend.codecs_for_resolution(480)
    assert codecs == []

def test_validate_url():
    backend = Backend(None)
    
    valid_urls = [
        "https://www.youtube.com/watch?v=bi4drICAjpM",
        "https://www.youtube.com/watch?v=bOFdIvuA4Eo",
        "https://youtu.be/F4tHL8reNCs"
    ]

    
    invalid_urls = [
        "just-text",
        "https://youtu.be/",
        "https://www.youtube.com/embed/",
        "https://www.youtube.com/v/",
        "not a url"
    ]
    
    for url in valid_urls:
        assert backend.validate_url(url) == True
    
    for url in invalid_urls:
        assert backend.validate_url(url) == False