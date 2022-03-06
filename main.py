from distutils.log import error
from argostranslate import package, translate
from multiprocessing import Pool
import subprocess
import os

package.install_from_path("translate-ja_en-1_1.argosmodel")
installed_languages = translate.get_installed_languages()

print([str(lang) for lang in installed_languages])
translator = installed_languages[1].get_translation(installed_languages[0])

def translate(origin_text):
    return translator.translate(origin_text)

data = {}
data[ord("。")] = 1
data[ord("、")] = 1
data[ord("」")] = 1
data[ord("―")] = 1
data[ord("？")] = 1

def build_dict(file_name):
    subprocess.run(f"./mjdisasm.exe {file_name}")
    base_name = file_name.split('.')[0]
    asm = open(f"{base_name}.mjs", 'r', encoding="utf8")
    pattern = "<(.*?)>"
    indexes = []
    for i in range(1, 1826):
        try:
            line = asm.readline()
            if line[0:24] == "call<$a4eb1e4c, 0> (#res":
                print(line[0:14])
                #temp = re.search(pattern, line[14:]).group(0)
                indexes.append(line[25:29])
                indexes.append(1)
                #print(temp)
        except EOFError:
            break

    words_dict = {indexes[i]: indexes[i+1] for i in range(0, len(indexes), 2)}
    words = open(f"{base_name}.sjs", 'r', encoding='cp932')
    final = {}
    for i in range(1, 1826):
        try:
            line = words.readline()
            if len(line) != 0:
                print(line[1:6])
            if words_dict.get(line[1:5]) == 1:
                temp = len(line)-1
                key = line[7:temp]
                key.encode('utf-8')
                final[key] = 1
        except EOFError:
            break
    words.close()
    asm.close()
    os.remove(f"{base_name}.mjs")
    os.remove(f"{base_name}.sjs")
    return final

def main(final_number):
    outfile = open(f"new_{final_number}.utf", "w", encoding="utf8")
    file = open(f"{final_number}.utf", "r", encoding='utf8')
    key_dict = build_dict(f"{final_number}.mjo")
    print(key_dict)
    print(len(key_dict))
    count = 0
    for i in range(1, 20000):
        try:
            filedata = file.readline()
            temp = [ord(c) for c in filedata.rstrip("\n")]
            # if filedata[0] != '<' and data.get(temp[len(temp)-2]) != 1:
            temp = len(filedata)-2
            if filedata[0] != '<':
                outfile.write(filedata)
                continue
            #if data.get(temp[-2]) != 1:
            #   outfile.write(filedata)
            #  continue
            print(filedata[7:temp])
            if key_dict.get(filedata[8:temp]) == 1: 
                print(i)
                count += 1
                outfile.write(filedata)
                continue
            else:
                translation = translate(filedata[7:temp])
                final = filedata.rstrip("\n")
                final += translation.rstrip("\n")
                final += "\n"
                outfile.write(final)
        except Exception as e:
            print(e)
            break
    print(count)
    outfile.close()
    file.close()
    os.remove(f"{final_number}.utf")
    os.rename(f"new_{final_number}.utf", f"{final_number}.utf")
    subprocess.run(f"./majiro.exe {final_number}.utf")
    subprocess.run(f"./majiro.exe {final_number}.mjo")


def test():
    string_test = "<$01E2> ４月と言えば、新学期。新入学シーズン。="
    temp = [ord(c) for c in string_test]
    print(ord("。"))
    print(ord("、"))
    print(ord("」"))
    print(ord("―"))
    print(data.get(temp[len(temp)-1]))
    print(temp)


def driver():
    args = []
    files = os.listdir("../new/")
    for file in files:
        if file.endswith(".mjo"):
            temp = file.split('.')[0]
            args.append(temp)


    for arg in args:
        print(arg)
        main(arg)
    

driver()
