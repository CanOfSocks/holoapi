html_template = '''
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>HoloAPi Docs</title>
    <!-- GitHub Markdown CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown-light.min.css">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            padding: 2rem;
            background-color: #f6f8fa;
        }
        .markdown-body {
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
            background: white;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(27,31,35,0.12);
        }
    </style>
</head>
<body>
    <article class="markdown-body">
        {{ content|safe }}
    </article>
</body>
</html>
'''