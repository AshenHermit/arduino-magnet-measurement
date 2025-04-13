from pathlib import Path


class RecordStep:
    def __init__(self, t, pos, digital, analog):
        self.time = t
        self.pos = pos
        self.digital = digital
        self.analog = analog
        self.values = [t, pos, digital, analog]

    @property
    def is_valid(self):
        for value in self.values:
            if value is None:
                return False
        return True


class RecordStepsPackage:
    def __init__(self, steps: list[RecordStep], name: str):
        self.steps: list[RecordStep] = steps
        self.name = name

    def plot(self, ax, x_prop, y_prop, label, color):
        x_values = []
        y_values = []
        for step in self.steps:
            x_values.append(step.__dict__[x_prop])
            y_values.append(step.__dict__[y_prop])
        ax.plot(x_values, y_values, label=label, color=color)


class RecordReader:
    def __init__(self, filepath: Path):
        self.filepath = Path(filepath)

    def parse_steps(self) -> RecordStepsPackage:
        steps = []
        text = self.filepath.read_text(encoding="utf-8")

        for line in text.strip().split("\n"):
            try:
                t, pos, digital, analog = map(float, line.split(" : "))
                step = RecordStep(t, pos, digital, analog)
                if step.is_valid:
                    steps.append(step)
            except:
                # print(f'line "{line}" is not valid to parse')
                pass

        steps_package = RecordStepsPackage(steps, self.filepath.stem)
        return steps_package


class MultiReader:
    def __init__(self, dir: Path):
        self.dir = Path(dir)

    def parse(self, glob_pattern="*.txt") -> list[RecordStepsPackage]:
        packages = []
        filepaths = list(self.dir.glob(glob_pattern))

        for filepath in filepaths:
            package = RecordReader(filepath).parse_steps()
            packages.append(package)

        return packages
