<h1 align="center">
    <img src="https://raw.githubusercontent.com/battleoverflow/shinigami/main/assets/shinigami_logo.png" />
</h1>

<p align="center">
    <b>Shinigami was created to be simplistic and maintainable</b>
</p>

Shinigami is an open source Python library allowing the user to generate and build Dockerfiles during runtime.

## Usage

You can install Shinigami via pip:

```bash
pip install shinigami
```

### Example

```python
from shinigami import Shinigami

def create_file():
    Shinigami(lang_os="python", version="3.9", build=True, verbose=True, color=True).generate_dockerfile()

if __name__ == '__main__':
    create_file()
```

If you just want to generate the Dockerfile without building the container, you can do that too. Just remove the `build` boolean from the class and you should see a Dockerfile populate in your current directory within seconds.

## CLI

### Usage

Available commands:

```
-h,  --help      |  Help menu
-i,  --image     |  Docker image to generate
-v,  --version   |  Version of the Docker image
-b,  --build     |  Build the Dockerfile after generation
-c,  --color     |  Generate color in the output
-rm, --remove    |  Remove the Dockerfile in your current working directory
```

### Examples

This command will generate a Dockerfile for Ubuntu 22.04, but won't build the Docker image
```bash
shinigami -i "ubuntu" -v "22.04"
```

This command will build a Docker image running Python 3.8 and generate the Dockerfile
```bash
shinigami -i "python" -v "3.8" -b
```

Removes the Dockerfile in your current working directory
```bash
shinigami -rm
```