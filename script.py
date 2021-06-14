import requests
import os
import subprocess

url='http://10.10.185.55/'

dir_head='.git/logs/HEAD'

def find_word(main_word,select_word):
    comodin=True
    for i in range(len(main_word)):
        if(main_word[i]==select_word[0]):
            for j in range(len(select_word)):
                if(i+j<len(main_word)):
                    if(main_word[i+j]!=select_word[j]):
                        comodin=False
                else:
                    comodin=False
        if(comodin==False):
            break
    return comodin

def select_by_delimit(palabra,delimit):
    lista_words=[]
    str_temp=""
    for i in range(len(palabra)):
        if(palabra[i]!=delimit):
            str_temp+=palabra[i]
        else:
            lista_words.append(str_temp)
            str_temp=""

        if(i==(len(palabra)-1)):
            lista_words.append(str_temp)
            break

    return lista_words 


def verify_dir_git():
    if(os.path.exists(".git/")):
        print(" ")
    else:
        os.system("git init")

def verify_dir(directorio):
    command="mkdir "
    if(os.path.exists(directorio)==False):
        command+=directorio
        os.system(command)

def reconstruct_file(hash,file,pathfile):
    hash_dir=hash[0]+hash[1]
    hash_object=""
    for i in range(2,len(hash)):
        hash_object+=hash[i]
    dir_download=url+".git/objects/"+hash_dir+"/"+hash_object
    verify_dir(".git/objects/"+hash_dir)
    command_curl="curl -s -X GET "+dir_download+" -o "+".git/objects/"+hash_dir+"/"+hash_object
    os.system(command_curl)
    command_git_cat="git cat-file -p "+hash+" 2>/dev/null"
    result_content=os.popen(command_git_cat).read()
    f = open(pathfile+file, "w")
    f.write(result_content)
    f.close()


def reconstruct_tree(object1,number):
    print(object1)
    dir_sha=object1[0]+object1[1]
    file_object=""
    for i in range(2,len(object1)):
        file_object+=object1[i]
    dir_object=".git/objects/"+dir_sha
    dir_download=dir_object+"/"+file_object
    # verificamos si existe y si no lo creamos
    verify_dir(dir_object)
    dir_download=url+dir_download
    command_curl="curl -s -X GET "+dir_download+" -o "+dir_object+"/"+file_object    
    os.system(command_curl)
    command_git_cat="git cat-file -p "+object1
    salida=os.popen(command_git_cat).read()

    lista_hashes=select_by_delimit(salida,'\n')
    lista_elements=select_by_delimit(lista_hashes[0],' ')
    #print(lista_elements[1])

    # creacion de directorio de reconstruccion :

    verify_dir("files_commits")
    verify_dir("files_commits/"+"commit"+str(number))
    pathfile="files_commits/"+"commit"+str(number)+"/"
    #reconstruir el hash que pertenece al tree
    
    dir_sha=lista_elements[1][0]+lista_elements[1][1]
    file_object=""
    for i in range(2,len(lista_elements[1])):
        file_object+=lista_elements[1][i]
    #print(file_object)
    dir_object=".git/objects/"+dir_sha
    verify_dir(dir_object)
    dir_download=url+dir_object+"/"+file_object
    command_curl="curl -s -X GET "+dir_download+" -o "+dir_object+"/"+file_object
    os.system(command_curl)
    command_git_cat="git cat-file -p "+dir_sha+file_object
    all_objects=os.popen(command_git_cat).read()
    all_files_in_commit=select_by_delimit(all_objects,'\n')
    
    white_list=['.php','.xml','.html','.md','.csv','.js','.json','.py','.c','.cpp','.h','.rb']
    
    for i in range(len(all_files_in_commit)-1):
        temp_list=select_by_delimit(all_files_in_commit[i],' ')
        print(temp_list[2])
        temp_list2=select_by_delimit(temp_list[2],'\t')
        for j in range(len(white_list)):
            if(find_word(temp_list2[1],white_list[j])):
                reconstruct_file(temp_list2[0],temp_list2[1],pathfile)
                break



def view_all_commits(url):
    r=requests.get(url=url)
    texto=r.text

    main_head=[]
    head_line=""
    for i in range(len(texto)):
        if(texto[i]!='\n'):
            head_line+=texto[i]
        else:
            main_head.append(head_line)
            head_line=""
    
    commits_all=[]
    for i in main_head:
        commits_all.append( select_by_delimit(i,' ') )

    print("Se encontraron",len(main_head),"commits")
    print("----------------------------------------")
    for i in range(len(commits_all)):
        print(i+1,"-> ",end="")
        for j in range(8,len(commits_all[i])):
            print(commits_all[i][j],end=" ")
        print("")
    print("----------------------------------------")

    num_commit=int(input("Que commit deseas reconstruir : "))

    reconstruct_tree(commits_all[num_commit-1][1],num_commit)


#rando=select_by_delimit("hola,nuevo,pum",',',2)
view_all_commits(url+dir_head)

#print(find_word("function.",".php"))


    
#for i in main_head:
#    print(i)
