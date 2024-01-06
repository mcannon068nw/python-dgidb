from dgidb import graph_app
import pytest

def test_generate_app():
    app = graph_app.generate_app()
    if __name__ == '__main__':
        app.run_server()