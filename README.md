## Installation for rtb-bidder

1. Clone rtb-bidder repository


2. Install `pyenv`, `pyenv-virtualenv` for activate an independent env for rtb-bidder

    ```sh
    $ brew install pyenv
    ```

    Upgrade pyenv to the latest

    ```sh
    $ brew update && brew upgrade pyenv
    ```
     Install Python 3.9.9.
    Before running this line, xcode maybe need to be installed and accepted. In new arch., behind SPE we need to add sudo.

    ```sh
    $ CONFIGURE_OPTS="--with-openssl=$(brew --prefix openssl)" pyenv install 3.9.9
    ```
   Create and activate a new virtualenv for rtb-bidder

    Install pyenv-virtualenv. It is a pyenv plugin that provides features to manage virtualenvs for Python on UNIX-like systems

    ```sh
    $ brew install pyenv-virtualenv
    ```

    Create a virtualenv which is named rtb-bidder for the current Python version used with pyenv

    ```sh
    $ pyenv virtualenv rtb-bidder
    ```

    Activate virtualenv which is named rtb-bidder

    ```sh
    $ pyenv activate rtb-bidder
    ```

3. Install project dependencies by requirement.txt

   ```shell
   $ pip install -r requirements.txt
   ```


## Run DB Container
1.
    ```shell
    $ docker-compose up -d
    ```
2. The output is the following:

    ```shell
    Starting api-server ... done
    ```


## Run rtb-bidder

```shell
# normal mode
$ python cli.py
```


Both the above commands will boot rtb-bidder service on `http://localhosl:3002/root`
The default response in root path will return the following JSON response

```json
{ "status": 0 }
```

### OpenAPI

The openapi spec generated by FastAPI can be browsed on `http://localhost:3002/docs`
