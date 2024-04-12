import fire
import os


class CLI(object):
    """PyToy CLI."""

    def hello(self, name: str = "World"):
        """Say hello."""
        print(f"Hello, {name}!")

    def replace_file(self, file: str, old: str, new: str, extension: str = None):
        if extension and not file.endswith(extension):
            return
        with open(file, "r") as f:
            text = f.read()
        text = text.replace(old, new)
        with open(file, "w") as f:
            f.write(text)

    def replace_dir(
        self,
        dir: str,
        old: str,
        new: str,
        extension: str = None,
        recursive: bool = False,
    ):
        for root, dirs, files in os.walk(dir):
            for file in files:
                file_path = os.path.join(root, file)
                self.replace_file(file_path, old, new, extension)

            if not recursive:
                break

            for subdir in dirs:
                subdir_path = os.path.join(root, subdir)
                self.replace_dir(subdir_path, old, new, extension, recursive)


def PyToy():
    fire.Fire(CLI)


if __name__ == "__main__":
    PyToy()
