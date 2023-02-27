"""
This module contains constants that are used in various parts of the project.

Global variables such as capture, rec_frame, grey, switch, neg, face, and rec are initialized to zero and used in the face recognition system.

The following constants are defined in this module:


- VALID_COURSE_CODES: A list of valid course codes for the lecturer.py module.
- TYPES: A list of strings representing the types of directories that can be created.
- VIDEO_EXTENSIONS: A list of video file extensions.
- DOC_EXTENSIONS: A list of document file extensions.
- ASSIGNMENT_EXTENSIONS: A list of file extensions that are valid for assignment submissions.
- ALLOWED_EXTENSIONS: A set of file extensions that are allowed for file uploads.
- COURSES_INFO: A dictionary containing information about each course offered in the project.

"""


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
TYPES = ["video", "assignment", "documents", "attendance", "registered_faces"]


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
        "course_name": "Neural Networks and Fuzzy Logic Programming",
        "info": """Neural networks and fuzzy logic programming are two approaches in
        artificial intelligence (AI) that enable machines to make intelligent
        decisions based on input data.\n

        Neural networks are computing systems inspired by the structure and
        function of the human brain. They are composed of interconnected nodes
        or neurons that are organized into layers. Each node processes incoming
        data and sends an output signal to other connected nodes. By adjusting
        the strength of connections between nodes, neural networks can learn
        from input data and make predictions or classifications.\n

        Fuzzy logic is a mathematical framework for dealing with uncertain or
        vague information. It uses degrees of truth or membership functions to
        model the uncertainty and imprecision of data. In fuzzy logic
        programming, rules are defined using linguistic variables and fuzzy
        sets, and the output of the program is a fuzzy set that represents the
        degree of membership of the input data to a particular class or
        category.\n

        Neural networks and fuzzy logic programming can be combined to create
        hybrid systems that take advantage of the strengths of both approaches.
        For example, a neural network can be trained using fuzzy logic-based
        inputs and outputs to make more accurate predictions or classifications
        in situations with uncertain or imprecise data.""",
        "doc_dir": "501/documents",
        "doc_exts": (
            ".doc",
            ".docx",
            ".pdf",
        ),
        "video_dir": "501/video",
        "video_ext": ".mp4",
    },
    "503": {
        "course_name": "Computer Aided Design",
        "info": """
        Computer-aided design (CAD) is the use of computer software to create,
        modify, analyze, and optimize designs. CAD software is used by
        architects, engineers, graphic designers, and other professionals to
        create 2D or 3D models of products, buildings, or other objects. CAD
        software allows designers to create more accurate and detailed designs
        than traditional manual drafting methods. CAD models can be easily
        modified and shared, making the design process more efficient and
        collaborative.
        """,
        "doc_dir": "503/documents",
        "doc_exts": (".doc", ".pdf"),
        "video_dir": "503/video",
        "video_ext": ".mp4",
    },
    "507": {
        "course_name": "Digital Signal Processing",
        "info": """
        Digital Signal Processing (DSP) is a technique for processing signals
        that have been converted from analog to digital form. It involves the
        manipulation of signals using mathematical algorithms and digital
        computation techniques to extract useful information, remove unwanted
        noise, enhance signal quality, or compress and transmit signals
        efficiently. DSP is widely used in many applications such as audio and
        image processing, speech recognition, radar, sonar, and biomedical
        signal processing. The basic steps in DSP include sampling and
        quantization of the signal, filtering, transform analysis, and signal
        synthesis. DSP techniques are implemented using specialized software or
        hardware devices called Digital Signal Processors (DSPs), which are
        optimized for high-speed, low-power signal processing tasks.        
        """,
        "doc_dir": "507/documents",
        "doc_exts": (".doc", ".pdf", ".docx"),
        "video_dir": "507/video",
        "video_ext": ".mp4",
    },
    "511": {
        "course_name": "Computer Graphics",
        "info": """
        Computer graphics refers to the field of computer science that involves creating, manipulating, and displaying visual content using computers. It involves using software tools and algorithms to create and modify digital images, animations, and videos. Computer graphics can be used for a wide range of purposes, including creating visual effects for movies, designing video games, creating 3D models for product design, and producing scientific visualizations. Computer graphics can be created using a variety of techniques, including 2D and 3D modeling, rendering, and animation.     
        """,
        "doc_dir": "511/documents",
        "doc_exts": (".doc", ".pdf", ".docx"),
        "video_dir": "511/video",
        "video_ext": ".mp4",
    },
    "505": {
        "course_name": "Software Engineering",
        "info": """
        Software engineering is the process of designing, creating, testing, and
        maintaining software. It involves a systematic approach to the
        development of software, with a focus on producing high-quality,
        reliable, and efficient software products that meet the needs of users.
        """,
        "doc_dir": "505/documents",
        "doc_exts": (".doc", ".pdf", ".docx"),
        "video_dir": "505/video",
        "video_ext": ".mp4",
    },
    "515": {
        "course_name": "Natural Language Processing",
        "info": """
        Natural Language Processing (NLP) is a field of study focused on developing algorithms and techniques that enable computers to understand, interpret, and generate human language. NLP involves combining techniques from linguistics, computer science, and artificial intelligence to create software that can analyze, process, and generate natural language text and speech. NLP algorithms can be used to perform tasks such as text classification, sentiment analysis, machine translation, speech recognition, and language generation. NLP has numerous applications in areas such as customer service, healthcare, education, and finance, and is a rapidly evolving field that continues to advance with the development of new machine learning models and data-driven approaches.       
        """,
        "doc_dir": "515/documents",
        "doc_exts": (".doc", ".pdf", ".docx"),
        "video_dir": "515/video",
        "video_ext": ".mp4",
    },
    "519": {
        "course_name": "Robotics",
        "info": """
        Robotics is a field of study and practice that involves the design, construction, and operation of robots. A robot is a machine that is capable of carrying out complex tasks, often with some degree of autonomy. Robotics draws on knowledge from multiple fields, including mechanical engineering, electrical engineering, and computer science. Robots can be designed for a wide range of applications, including manufacturing, healthcare, transportation, and exploration.     
        """,
        "doc_dir": "519/documents",
        "doc_exts": (".doc", ".pdf", ".docx"),
        "video_dir": "519/video",
        "video_ext": ".mp4",
    },
}
