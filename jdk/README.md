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

С Oracle часто возникают различные проблемы, в частности, не принимаются Cookie соглашения с лицензией, либо облако просто не позволяет скачивать, даже если всё в порядке.

Так что, для гарантии успеха деплоя, единожды скачиваем требуемый jdk-...windows-x...exe на управляющую систему и рассылаем файл с неё.

    ansible-playbook prepare.yml -e jdk_exe="~/Downloads/jdk-8u111-windows-x64.exe" -e java_version=8 -e java_build=111

В вышеприведенном примере у нас есть скачанный jdk для java8 билд 111, который копируется на хост в C:\, после чего устанавливается.

Чтобы один и тот же jdk не устанавливался несколько раз, используется product_id (по умолчанию прописан для jdk-8u111-windows-x64.exe, так что его в этом примере можно не указывать)

java_version и java_build необходимы для корректной генерации Product_Id для реестра Windows. Вместо них прямо указать `-e product_id="{00....}"` для конкретного пакета jdk.
Product_Id можно увидеть на установленной системе в реестре по пути `HKLM:Software\Microsoft\Windows\CurrentVersion\Uninstall`
