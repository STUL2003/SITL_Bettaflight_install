# SITL_Bettaflight_install
** Инструкция по установке Bettaflight_SITL **
___________________________________________________________________
Клонируем репозиторий
```bash
git clone https://github.com/betaflight/betaflight.git
cd betaflight
```
____________________________________________________________________
Временно добавить Google DNS, устанавливаем ARM GCC и собираем проект
```bash
sudo sh -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
make arm_sdk_install
make configs
make TARGET=SITL sim
```
____________________________________________________________________
В первом терминале запускаем:
```bash
./obj/main/betaflight_SITL.elf
```
В втором запускаем:
```bash
git clone https://github.com/novnc/websockify-other.git
cd websockify-other/c
make
./websockify 127.0.0.1:6761 127.0.0.1:5761
```
__________________________________________________________________
Онлайн конфигуратор не работает, поэтому скачиваем отсюда:
https://github.com/betaflight/betaflight-configurator/releases/tag/10.10.0
__________________________________________________________________
Устанавливаем пакет  и необходимые зависимости:
```bash
sudo dpkg -i betaflight-configurator_10.10.0_amd64.deb
```
