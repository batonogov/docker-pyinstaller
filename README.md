# PyInstaller Docker Images

**batonogov/pyinstaller-linux**, **batonogov/pyinstaller-windows** and **batonogov/pyinstaller-osx (Experimental)**
are a trio of Docker containers to ease compiling Python applications to binaries / exe files.

## Tags

Images have few tags:

| Image                                                          | TAG                      | Python  | Pyinstaller |
| -------------------------------------------------------------- | ------------------------ | ------- | ----------- |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:v4.1.1`                | 3.12.1  | 6.3.0       |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:v4.1.0`                | 3.12.0  | 6.3.0       |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:v4.0.1`                | 3.11.7  | 6.3.0       |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:v4.0.0`                | 3.11.6  | 6.3.0       |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:v3.3.1`                | 3.11.6  | 6.3.0       |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:v3.3.0`                | 3.11.6  | 6.2.0       |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:python-3.11`/`:v3.2.1` | 3.11.6  | 6.0.0       |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:v3.2.0`                | 3.11.5  | 6.0.0       |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:3.1.6`                 | 3.11.5  | 5.13.2      |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:3.1.5`                 | 3.11.5  | 5.13.1      |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:3.1.4`                 | 3.11.4  | 5.13.0      |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:3.1.3`                 | 3.11.4  | 5.12.0      |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:3.1.1`                 | 3.11.3  | 5.11.0      |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:3.1.0`                 | 3.11.3  | 5.9.0       |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:3.0.2`                 | 3.11.2  | 5.8.0       |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:3.0.1`                 | 3.11.1  | 5.7.0       |
| `batonogov/pyinstaller-linux`, `batonogov/pyinstaller-windows` | `:python-3.10`           | 3.10.10 | 5.7.0       |

**batonogov/pyinstaller-osx (Experimental) have tags:

| Image                       | TAG       | Python  | Pyinstaller |
| --------------------------- | --------- | ------- | ----------- |
| `batonogov/pyinstaller-osx` | `:v4.1.0` | 3.11.3  | 6.3.0       |
| `batonogov/pyinstaller-osx` | `:v4.0.1` | 3.11.3  | 6.3.0       |
| `batonogov/pyinstaller-osx` | `:v4.0.0` | 3.11.3  | 6.3.0       |

## Usage

There are two containers, one for Linux and one for Windows and one forx osx builds.
The Windows builder runs Wine inside Ubuntu to emulate Windows in Docker.
The osx builder used sickcodes/docker-osx base image.

To build your application, you need to mount your source code into the `/src/` volume.

The source code directory should have your `.spec` file that PyInstaller generates. If you don't have one, you'll need to run PyInstaller once locally to generate it.

If the `src` folder has a `requirements.txt` file, the packages will be installed into the environment before PyInstaller runs.

For example, in the folder that has your source code, `.spec` file and `requirements.txt`:

```console
docker run -v "$(pwd):/src/" batonogov/pyinstaller-windows
```

will build your PyInstaller project into `dist/`. The `.exe` file will have the same name as your `.spec` file.

```console
docker run -v "$(pwd):/src/" batonogov/pyinstaller-linux
```

will build your PyInstaller project into `dist/`. The binary will have the same name as your `.spec` file.
### How do I specify the spec file from which the executable should be build?

You'll need to pass an environment variable called `SPECFILE` with the path (relative or absoulte) to your spec file, like so:

```console
docker run -v "$(pwd):/src/" -e SPECFILE=./main-nogui.spec batonogov/pyinstaller-linux
```

This will build the executable from the spec file `main-nogui.spec`.

### How do I install system libraries or dependencies that my Python packages need?

You'll need to supply a custom command to Docker to install system pacakges. Something like:

```console
docker run -v "$(pwd):/src/" --entrypoint /bin/sh batonogov/pyinstaller-linux -c "apt update -y && apt install -y wget && /entrypoint.sh"
```

Replace `wget` with the dependencies / package(s) you need to install.

### How do I generate a .spec file?

`docker run -v "$(pwd):/src/" batonogov/pyinstaller-linux "pyinstaller --onefile your-script.py"`

will generate a `spec` file for `your-script.py` in your current working directory. See the PyInstaller docs for more information.

### How do I change the PyInstaller version used?

Add `pyinstaller==6.2.0` to your `requirements.txt`.

### Is it possible to use a package mirror?

Yes, by supplying the `PYPI_URL` and `PYPI_INDEX_URL` environment variables that point to your PyPi mirror.

## History

Now release information will be [here](https://github.com/batonogov/docker-pyinstaller/releases).

Release History

<details>
  <summary>2023</summary>

### [3.1.0] - 08.04.2023

- Linux container now uses Python base image
- Updated Pyintaller 5.8.0 -> 5.9.0
- Updated Python 3.11.2 -> 3.11.3

#### [3.0.2] - 13.02.2023

- Updated Python 3.11.1 -> 3.11.2
- Updated Ubuntu 20.04 -> 22.04 for windows
- Updated Pyintaller 5.7.0 -> 5.8.0

#### [3.0.1] - 24.01.2023

- New GitHub CI
- Added arm64 architecture in linux images

#### [3.0.0] - 01.01.2023

- Semver now
- Updated Pyintaller 5.5.0 -> 5.7.0
- Updated Python 3.10.8 -> 3.11.1

</details>

<details>
  <summary>2022</summary>

#### [2.9] - 2022-10-21

- Python is compiled from sources
- Updated GitHub Actions (testing the image before push)
- Removed OpenSSL
- Updated Python 3.10.6 -> 3.10.8
- Updated Pyintaller 5.3.0 -> 5.5.0
- Optimized Dockerfiles

#### [2.8] - 2022-08-11

- Updated OpenSSL 1.1.1p -> 1.1.1q
- Updated Pyinstaler 5.2.0 -> 5.3.0
- Updated Python 3.10.5 -> 3.10.6

#### [2.7] - 2022-07-10

- Updated Python 3.10.4 -> 3.10.5
- Updated OpenSSL 1.1.1o -> 1.1.1p
- Updated Pyinstaler 5.1.0 -> 5.2.0

#### [2.6] - 2022-05-18

- Updated Pyinstaler 4.10 -> 5.1.0
- Updated OpenSSL 1.1.1n -> 1.1.1o

#### [2.5] - 2022-04-15

- Updated Ubuntu 20.04 -> 22.04 for amd64
- Updated Python 3.10.1 -> 3.10.4
- Updated Pyinstaler 4.7.0 -> 4.10
- Updated OpenSSL 1.1.1m -> 1.1.1n

</details>

<details>
  <summary>2021</summary>

#### [2.4] - 2021-12-23

- Updated Python 3.10.0 -> 3.10.1
- Updated OpenSSL 1.1.1l -> 1.1.1m

#### [2.3] - 2021-11-14

- Updated Python 3.9.7 -> 3.10.0
- Updated Pyinstaler 4.5.1 -> 4.7.0

#### [2.2] - 2021-10-16

- Updated Ubuntu 12.04 -> 20.04 for amd64
- Updated openssl 1.0.2u -> 1.1.1l for amd64
- Deleted Python 2 Dockerfiles
- Deleted 32 bit Dockerfiles

#### [2.1] - 2021-09-24

- Updated Ubuntu 16.04 -> 20.04 for win64 and win32
- Updated PyInstaller 4.2 -> 4.5.1
- Updated Python 3.9.5 -> 3.9.7

#### [2.0] - 2021-03-11

- Drop support for Python 2.7
- Updated Python 3 to version 3.9
- Updated PyInstaller to version 4.2

</details>

<details>
  <summary>2020</summary>

#### [1.9] - 2020-01-14

- Added a 32bit package, thank you @danielguardicore
- Updated PyInstaller to version 3.6

</details>

<details>
  <summary>2019</summary>

#### [1.8] - 2019-01-15

- Build using an older version of glibc to improve compatibility, thank you @itouch5000
- Updated PyInstaller to version 3.4

</details>

<details>
  <summary>2018</summary>

#### [1.7] - 2018-10-02

Bumped Python version to 3.6 on Linux, thank you @itouch5000

</details>

<details>
  <summary>2017</summary>

#### [1.6] - 2017-11-06

Added Python 3.6 on Windows, thanks to @jameshilliard

#### [1.5] - 2017-09-29

Changed the default PyInstaller version to 3.3

#### [1.4] - 2017-01-26

Fixed bug with concatenated commands in entrypoint arguments, thanks to @alph4

#### [1.3] - 2017-01-23

Upgraded PyInstaller to version 3.2.1.
Thanks to @bmustiata for contributing:

- Custom PyPi URLs
- No longer need to supply a requirements.txt file if your project doesn't need it
- PyInstaller can be called directly, for e.g to generate a spec file

</details>

<details>
  <summary>2016</summary>

#### [1.2] - 2016-12-13

Added Python 3.5 on Windows, thanks (again) to @bmustiata

#### [1.1] - 2016-12-13

Added Python 3.4 on Windows, thanks to @bmustiata

#### [1.0] - 2016-08-26

First release, works.

</details>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=batonogov/docker-pyinstaller&type=Date)](https://star-history.com/#batonogov/docker-pyinstaller&Date)

## License

MIT
