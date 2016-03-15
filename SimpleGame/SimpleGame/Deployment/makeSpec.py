import os
import sys



currentDir = os.path.dirname(sys.argv[0])
dir = os.path.join(currentDir, '..', 'Assets')
dir = os.path.abspath(dir)

assets = os.walk(dir)

items = []
for root, subFolders, files in assets:
    for file in files:
        path = root.replace(dir + '\\', '').replace('\\', '\\\\')
        
        item = "('..\\\\Assets\\\\{0}\\\\{1}', 'Assets\\\\{0}')".format(path, file)
        extension = os.path.splitext(file)[1]
        if extension in ['.png', '.json', '.ttf', '.otf', '.wav', '.mp3']:
            items.append(item)
        else:
            print('Not included: {0}'.format(file))

result = ",\n".join(items)

sourcefile = os.path.join(currentDir, "Game.spec.pattern")
destFile = os.path.join(currentDir, "Game.spec")

with open(sourcefile) as f:
    newText=f.read().replace('{{FILES}}', result)

with open(destFile, "w") as f:
    f.write(newText)


print("Spec-Datei erzeugt!")



