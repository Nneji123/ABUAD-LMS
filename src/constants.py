global capture, rec_frame, grey, switch, neg, face, rec, out
capture = 0
grey = 0
neg = 0
face = 0
switch = 1
rec = 0


# constants for lecturer.py
VALID_COURSE_CODES = ["501", "503", "515", "507", "511", "505", "519"]

# create a function to make new directories from a list of strings
TYPES = ["video", "assignment", "documents", "attendance"]


VIDEO_EXTENSIONS = [
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".flv",
    ".wmv",
    ".webm",
    ".mpeg",
    ".mpg",
    ".m4v",
    ".3gp",
    ".3g2",
    ".f4v",
    ".f4p",
    ".f4a",
    ".f4b",
]
DOC_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".doc",
    ".csv",
]
ASSIGNMENT_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".doc",
    ".csv",
    ".txt",
    ".pptx",
    ".ppt",
    ".xlsx",
    ".xls",
    ".zip",
    ".rar",
    ".7z",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    ".iso",
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".flv",
    ".wmv",
    ".webm",
    ".mpeg",
    ".mpg",
    ".m4v",
    ".3gp",
    ".3g2",
    ".f4v",
    ".f4p",
    ".f4a",
    ".f4b",
]
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

COURSES_INFO = {
    "501": {
        "doc_dir": "501/documents",
        "doc_exts": (
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
            ".pdf",
            ".py",
            ".java",
            ".c",
            ".cpp",
            ".h",
        ),
        "video_dir": "501/video",
        "video_ext": ".mp4",
    },
    "503": {
        "doc_dir": "503/documents",
        "doc_exts": (".doc",),
        "video_dir": "503/video",
        "video_ext": ".mp4",
    },
    "507": {
        "doc_dir": "507/documents",
        "doc_exts": (".doc",),
        "video_dir": "507/video",
        "video_ext": ".mp4",
    },
}
