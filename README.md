# chkpt
A <sub>tiny</sub> pipeline builder

## What

`chkpt` is a zero-dependency, 100-line library that makes it easy to define and execute checkpointed pipelines.

It features...

* Fluent pipeline construction
* Transparent caching of expensive operations
* JSON serialization

## How

#### Defining a `Stage`

`Stage`s are the atomic units of work in `chkpt` and correspond to single Python functions. Existing functions need only use a decorator `@chkpt.Stage.wrap()` to be used as a `Stage`:

```python
@chkpt.Stage.wrap()
def stage1():
  return "123"

# stage1 is now a Stage instance
assert isinstance(stage1, chkpt.Stage)

# but the original function is still accessible
assert stage1.func() == "123"
```

`Stage`s can also accept parameters to be provided by other `Stage`s in the final `Pipeline`:

```python
@chkpt.Stage.wrap()
def stage2(stage1_input):
  return [stage1_input, "456"]
```

#### Defining a `Pipeline`

`Pipeline`s define the excution graph of `Stage`s to be run. `Stage`s are combined with shift operators (`<<` and `>>`) to direct the dataflow:

```python
# Each defines a pipeline calculating `stage1` and passing its output to `stage2`.
pipeline = stage1 >> stage2
pipeline = stage2 << stage1
pipeline = stage2 << (stage1,)
pipeline = (stage1,) >> stage2
pipeline = () >> stage1 >> stage2 
```

More complex pipelines should be defined from the leaves down:

```python
result1 = (stage1, stage2) >> stage3
result2 = (result1, stage1) >> stage4
pipeline = result2 >> stage5
```

#### Executing a `Pipeline`

`Pipeline`s can be directly executed which will use the default config settings:

```python
result = pipeline()
```

The defaults can be configured by passing a `Config` instance:

```python
# Will store all stage results and attempt to load already-stored results, if present.
result = pipeline(chkpt.Config(store=True, load=True, dir='/tmp'))
```

#### Examples

For detailed usage, see the [examples/]() directory.

The following is a brief example pipeline:

```python
import chkpt


@chkpt.Stage.wrap()
def make_dataset1():
  ...

@chkpt.Stage.wrap()
def big_download2():
  ...

@chkpt.Stage.wrap()
def work_in_progress_analysis(dataset1, dataset2):
  ...

pipeline = (make_dataset1, big_download2) >> work_in_progress_analysis
# Work-intensive inputs only run once, caching on reruns.
result = pipeline(chkpt.Config(load=[make_dataset1, big_download2]))
```
