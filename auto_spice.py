import matplotlib.pyplot as plt
import os, argparse, re
from rawfile import RawFile

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-c", "--circuit", help="Circuit file")
    argParser.add_argument("-s", "--spice", help="Spice")
    argParser.add_argument("--save", help="Save plot to file", action="store_true")

    config = argParser.parse_args()
    if config.spice:
        config.spice = config.spice.replace("\\n", "\n")
        with open("tmp.sp", "w", encoding="utf-8") as file:
            file.write(config.spice)
        config.circuit = "tmp.sp"

    os.system("ngspice -b -r test.raw " + config.circuit)
    rawFile = RawFile("test.raw")
    rawFile.open()
    rawFile.read()
    rawFile.close()
    os.remove("test.raw")

    time = rawFile.get_time_data()
    vars = []
    with open(config.circuit, "r", encoding="utf-8") as file:
        pattern = re.compile(r"plot\s+(.*)")
        for line in file:
            match = pattern.match(line)
            if match:
                vars.append(match.group(1).lower())
    curves = rawFile.get_curve_data(vars)

    if os.path.exists("tmp.sp"):
        os.remove("tmp.sp")

    if len(curves) > 0:
        figure, axes = plt.subplots(len(curves))
        figure.suptitle(rawFile.title + " [" + rawFile.plotName + "]")

        xlabel = "Time / s"
        ylabel = None
        if len(curves) > 1:
            for i, curve in enumerate(curves):
                ylabel = curve["name"]
                scale = max(abs(max(curve["data"])), abs(min(curve["data"])))
                if scale > 2e5:
                    axes[i].plot(time, [x / 1e6 for x in curve["data"]])
                    ylabel += " / M"
                elif scale > 2e2:
                    axes[i].plot(time, [x / 1e3 for x in curve["data"]])
                    ylabel += " / k"
                elif scale > 2e-1:
                    axes[i].plot(time, curve["data"])
                    ylabel += " / "
                elif scale > 2e-4:
                    axes[i].plot(time, [x * 1e3 for x in curve["data"]])
                    ylabel += " / m"
                elif scale > 2e-7:
                    axes[i].plot(time, [x * 1e6 for x in curve["data"]])
                    ylabel += " / μ"

                if curve["name"][0] == "v":
                    ylabel += "V"
                elif curve["name"][0] == "i":
                    ylabel += "A"

                axes[i].set_ylabel(ylabel)
                axes[i].set_xlabel("Time / s")
                axes[i].grid()
        else:
            ylabel = curves[0]["name"]
            scale = max(abs(max(curves[0]["data"])), abs(min(curves[0]["data"])))
            if scale > 2e5:
                plt.plot(time, [x / 1e6 for x in curves[0]["data"]])
                ylabel += " / M"
            elif scale > 2e2:
                plt.plot(time, [x / 1e3 for x in curves[0]["data"]])
                ylabel += " / k"
            elif scale > 2e-1:
                plt.plot(time, curves[0]["data"])
                ylabel += " / "
            elif scale > 2e-4:
                plt.plot(time, [x * 1e3 for x in curves[0]["data"]])
                ylabel += " / m"
            elif scale > 2e-7:
                plt.plot(time, [x * 1e6 for x in curves[0]["data"]])
                ylabel += " / μ"

            if curves[0]["name"][0] == "v":
                ylabel += "V"
            elif curves[0]["name"][0] == "i":
                ylabel += "A"

            plt.ylabel(ylabel)
            plt.xlabel("Time / s")
            plt.grid()

        if config.save:
            rawFile.title = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "", rawFile.title)
            plt.savefig(rawFile.title + ".png")
        else:
            plt.show()
    else:
        print("No curves to show.")
