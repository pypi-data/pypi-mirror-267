### Install

```bash
pip install cyzutils
```

### Usage

```python
from cyzutils import send_email

send_email('subject', 'content', 'xxxxxxx@xxx.xx')
```

### 打包上传 pypi 命令

```shell
pip install build

python -m build

pip install twine

twine check dist/*

twine upload dist/*
```

https://juejin.cn/post/7053009657371033630