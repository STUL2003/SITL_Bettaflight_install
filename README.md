# SITL_Bettaflight_install
**Инструкция по установке Bettaflight_SITL**
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
Настройка газебы (Не было связи из-за ошибки: [Err] [SystemLoader.cc:92] Failed to load system plugin [BetaflightPlugin] : Could not find shared library. быи только исходники):
```bash
cd ~/betaflight_gazebo
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```
Проверить наличие образа:
```bash
find . -type f -name '*.so' -print
```

Переменные для запуска:
```bash
export GZ_PLUGIN_PATH=~/betaflight_gazebo/build:$GZ_PLUGIN_PATH
export LD_LIBRARY_PATH=~/betaflight_gazebo/build:$LD_LIBRARY_PATH
```
__________________________________________________________________
Запуск газебы
```bash
gz sim -v4 -r ~/betaflight_gazebo/worlds/iris_runway_betaflight.sdf
```
__________________________________________________________________
Переписал исходники бетафлай, теперь пересборка:
```bash
cd ~/betaflight_gazebo
cp src/BetaflightPlugin.cc src/BetaflightPlugin.cc.bak
```
Потом снова к настройке газебы
