# JDK

Установка open_jdk и oracle_jdk

    ansible-playbook prepare.yml

## Open JDK

Устанавливается только на linux, как default-jdk пакет

## Oracle JDK

### Ubuntu

Установка за счёт репозитория webupd8team/java

Для установки конкретной версии - передать параметр `-e java_version=7`

Для выбора системной java:

+ Oracle: `ansible-playbook choose_java.yml -e java=8-oracle`
+ OpenJDK: `ansible-playbook choose_java.yml -e java=8-openjdk-amd64`

e.t.c

## Windows

Для работы ansible с windows необходимо разрешить winrm на порту 5986 для удаленного управления через PowerShell (например, с помощью предоставленного ansible [powershell скрипта](https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1)) и на управляющей системе установить пакет pywinrm (`pip install pywinrm`)

> Чтобы эти настройки применлись на Windows 7, требуется обновить Powershell до версии 3. (например с помощью [скрипта](https://github.com/ansible/ansible/blob/devel/examples/scripts/upgrade_to_ps3.ps1), (требуется .NET4) )
> У меня служба обновлений Windows 7 долго не работала, пока не поставил пакет Windows6.1-KB3172605-x64
> После того, как поставлен PS3 - работать так же, как и с win 10

Для установки oracle java необходимо указать версию java, версию jdk и номер билда:

    ansible-playbook prepare.yml -e java_version=8 -e java_build=111 -e java_internal_build=14

В вышеприведенном примере скачается jdk-8u111-windows-x64.exe (b14) на хост в C:\, после чего устанавливится.

Чтобы один и тот же jdk не устанавливался несколько раз, используется product_id (по умолчанию прописан для jdk-8u111-windows-x64.exe, так что его в этом примере можно не указывать)

java_version и java_build необходимы для корректной генерации ссылки для скачивания и Product_Id для реестра Windows. Можно также прямо указать `-e product_id="{00....}"` для конкретного пакета jdk.
Product_Id можно увидеть на установленной системе в реестре по пути `HKLM:Software\Microsoft\Windows\CurrentVersion\Uninstall`
