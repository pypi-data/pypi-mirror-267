# django-bootstrap-email

## Usage

1. Install

```shell
pip install django-bs-email
```

2. Add to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    # ...
    "django_bootstrap_email",
]
```

3. Use the template tag

```html
{% load bootstrap_email %}

{% bootstrap_email %}
<body class="bg-light">
  <div class="container">
    <div class="card my-10">
      <div class="card-body">
          <p>
            Hello World!
          </p>
      </div>
    </div>
  </div>
</body>
{% end_bootstrap_email %}
```

And a complete HTML email will be output, which should render correctly across email clients:

![Rendered HTML email example](https://raw.githubusercontent.com/jhthompson/django-bootstrap-email/main/example.png)