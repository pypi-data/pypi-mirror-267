import json, time

class CustomAnimation:
    def __init__(self, *, name:str, json_file_path:str, delay:float, loop:bool):
        self.name = name
        self.delay = delay
        self.jsonFilePath = json_file_path
        self.loop = loop
        print('\n\n')
        with open(self.jsonFilePath, 'r') as file:
            self.data = json.load(file)
            self.lastFrame = int(max(map(int, self.data["frames"].keys())))
            self.cla = int(len(self.data["frames"]["0"]))
            
        if not self.loop:
            for i in range(self.lastFrame+1):
                self.clearLastLines()
                self.frameContent = self.data["frames"][str(i)]
                print('\n'.join(self.frameContent.values()))
                time.sleep(self.delay)

        elif self.loop:
            i = 0
            while True:
                self.clearLastLines()
                self.frameContent = self.data["frames"][str(i)]
                print('\n'.join(self.frameContent.values()))
                time.sleep(self.delay)
                
                i += 1
                if i > self.lastFrame:
                    i = 0

    def clearLastLines(self):
        for _ in range(self.cla):
            print("\033[F\033[K", end="")
