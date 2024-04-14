# celery-streaming-result

Celery任务结果分片管理。

## 安装

```
pip install celery-streaming-result
```

## 使用方法

### 服务端

```python
import time
import redis
from celery.app import app_or_default
from celery_streaming_result import CeleryStreamingResultManager

app = app_or_default()
redis_instance = redis.Redis()
csrm = CeleryStreamingResultManager(redis_instance)

@app.task(bind=True)
def task1(celery_task):
    result = []
    for i in range(10):
        csrm.append_result_chunk(celery_task, i)
        result.append(i)
    csrm.append_ended_chunk(celery_task)
    return result

```

## 客户端

```python
import redis
from celery.app import app_or_default
from celery_streaming_result import CeleryStreamingResultManager
from test_server import task1 # 根据你的task定义，正确引用

app = app_or_default()
redis_instance = redis.Redis()
csrm = CeleryStreamingResultManager(redis_instance)

atask1 = task1.delay() # 生成一个异步任务
for chunk in csrm.get_result_chunks(atask1): # 读取该异步任务的结果分片
    print(chunk, end="-", flush=True)

```

## 版本记录

### v0.1.0

1. 首次发布。
