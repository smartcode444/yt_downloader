
from main.handler import VideoHandler

def test_handler():
    videohandler = VideoHandler()
    assert videohandler is not None

def test_fetch_metadata():
    url = "https://youtu.be/YA4X2PJRYCM?si=EroWUneTEs6YHW1I"
    videohandler = VideoHandler()  # Example YouTube URL
    videohandler.fetch_metadata(url)
    metadata = videohandler.metadata
    
    assert metadata is not None
    assert isinstance(metadata, dict)
    assert isinstance(metadata['formats'], list)
    assert len(metadata) > 0
    assert len(metadata['formats']) > 0
    assert 'id' in metadata
    assert 'title' in metadata
    assert 'formats' in metadata

def test_parse_formats():
    videohandler = VideoHandler()
    url = "https://youtu.be/YA4X2PJRYCM?si=EroWUneTEs6YHW1I"  # Example YouTube URL
    formats = videohandler.fetch_metadata(url)
    
    assert formats is not None
    assert isinstance(formats, list)
    assert len(formats) > 0
    for fmt in formats:
        assert 'id' in fmt
        assert 'res' in fmt
        assert 'fps' in fmt
        assert 'vcodec_raw' in fmt
        assert 'vcodec_name' in fmt
        assert 'size' in fmt

def test_parse_formats_with_invalid_url():
    videohandler = VideoHandler()
    url = "https://invalid-url.com/video"
    
    try:
        videohandler.fetch_metadata(url)
        assert False, "Expected an exception for invalid URL"
    except Exception as e:
        assert str(e) != ""  # Ensure an error message is provided