# PyInstaller Docker Images

**batonogov/pyinstaller-linux** and **batonogov/pyinstaller-windows**
are Docker/Podman containers designed to simplify the process of compiling Python applications into binaries/executables.

## Container registry

Images available on multiple container registry:

- [hub.docker.com](https://hub.docker.com/u/batonogov)

  - `batonogov/pyinstaller-windows` / `docker.io/batonogov/pyinstaller-windows`
  - `batonogov/pyinstaller-linux` / `docker.io/batonogov/pyinstaller-linux`

- [ghcr.io](https://github.com/batonogov?tab=packages&repo_name=docker-pyinstaller)

  - `ghcr.io/batonogov/pyinstaller-windows`
  - `ghcr.io/batonogov/pyinstaller-linux`

For linux images have slim and bullseye/bookworm version will ensure better compatibility.

- `-slim`
- `-slim-bookworm`
- `-slim-bullseye`

## Usage

There are three containers, one for `Linux` and one for `Windows` builds.
The Windows builder runs `Wine` inside Ubuntu to emulate Windows in Docker.

To build your application, you need to mount your source code into the `/src/` volume.

The source code directory should have your `.spec` file that PyInstaller generates. If you don't have one, you'll need to run PyInstaller once locally to generate it.

If the `src` folder has a `requirements.txt` file, the packages will be installed into the environment before PyInstaller runs.

For example, in the folder that has your source code, `.spec` file and `requirements.txt`:

```sh
docker run \
  --volume "$(pwd):/src/" \
  batonogov/pyinstaller-windows:latest
```

will build your PyInstaller project into `dist/`. The `.exe` file will have the same name as your `.spec` file.

```sh
docker run \
  --volume "$(pwd):/src/" \
  batonogov/pyinstaller-linux:latest
```

will build your PyInstaller project into `dist/`. The binary will have the same name as your `.spec` file.

### How do I specify the spec file from which the executable should be build?

You'll need to pass an environment variable called `SPECFILE` with the path (relative or absoulte) to your spec file, like so:

```sh
docker run \
  --volume "$(pwd):/src/" \
  --env SPECFILE=./main-nogui.spec \
  batonogov/pyinstaller-linux:latest
```

This will build the executable from the spec file `main-nogui.spec`.

### How do I install system libraries or dependencies that my Python packages need?

You'll need to supply a custom command to Docker to install system pacakges. Something like:

```sh
docker run \
  --volume "$(pwd):/src/" \
  --entrypoint /bin/sh batonogov/pyinstaller-linux:latest \
  -c "apt update -y && apt install -y wget && /entrypoint.sh"
```

Replace `wget` with the dependencies / package(s) you need to install.

### How do I generate a .spec file?

```sh
docker run \
  --volume "$(pwd):/src/" \
  batonogov/pyinstaller-linux:latest \
  "pyinstaller --onefile your-script.py"
```

will generate a `spec` file for `your-script.py` in your current working directory. See the PyInstaller docs for more information.

### How do I change the PyInstaller version used?

Add `pyinstaller==6.9.0` to your `requirements.txt`.

### Is it possible to use a package mirror?

Yes, by supplying the `PYPI_URL` and `PYPI_INDEX_URL` environment variables that point to your PyPi mirror.

### How do I use image in GitLab CI?

See [example](.gitlab-ci.yml) for GitLab CI.

```yaml
windows_bin:
  stage: deploy
  image:
    name: batonogov/pyinstaller-windows:latest
    entrypoint: ['']
  script:
    - echo "Creating Windows artifact"
    - pip install -r ./test/requirements.txt
    - cd ./test && pyinstaller --onefile main.py
    - cp ./dist/*.exe ../
  rules:
    - when: always
  artifacts:
    paths:
      - '*.exe'
    when: always
    expire_in: 2 week
```

### How do I use image in Bitbucket CI?

[Bitbucket doesn't support custom entrypoints](https://confluence.atlassian.com/bbkb/bitbucket-pipelines-does-not-execute-the-build-image-s-entrypoint-cmd-script-1299910012.html),
so we need to manually call it. Otherwise the setup is similar to what you would
do with GitLab CI.

```yaml
pipelines:
  default:
    - step:
        name: Build Windows executable
        image: batonogov/pyinstaller-windows:latest
        artifacts:
          paths:
            - *.exe
        script:
          - echo "Creating Windows artifact"
          - SPECFILE="$BITBUCKET_CLONE_DIR/sparvio-logger-bootstrap.spec" WORKDIR="$BITBUCKET_CLONE_DIR" bash /entrypoint.sh
          - pip install -r ./test/requirements.txt
          - cd ./test && pyinstaller --onefile main.py
          - cp ./dist/*.exe ../
```

## Known Issues

[ntdll.so Path Missing](https://github.com/batonogov/docker-pyinstaller/issues/23)

[Outdated Microsoft C++ Build Tools](https://github.com/batonogov/docker-pyinstaller/issues/11)

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

<a href="https://star-history.com/#batonogov/docker-pyinstaller&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=batonogov/docker-pyinstaller&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=batonogov/docker-pyinstaller&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=batonogov/docker-pyinstaller&type=Date" />
 </picture>
</a>

## License

MIT
