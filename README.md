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
В втором запускаем прокси, чтобы одновремено сидеть в конфигураторе, и проверять код:
```bash
python3 samo_betaflight/proxy_.py
```
В третьем запускаем:
```bash
# git clone https://github.com/novnc/websockify-other.git
cd websockify-other/c
# make
# Новый порт
./websockify 127.0.0.1:6761 127.0.0.1:5765
```
_____________________________________________________________
Настройка газебы (Не было связи из-за ошибки: [Err] [SystemLoader.cc:92] Failed to load system plugin [BetaflightPlugin] : Could not find shared library. быи только исходники):
```bash
cd ~/betaflight_gazebo
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
# Проверить наличие образа:
find . -type f -name '*.so' -print
```

Переменные для запуска и запуск в четвертом терминале:
```bash
export GZ_PLUGIN_PATH=~/betaflight_gazebo/build:$GZ_PLUGIN_PATH
export LD_LIBRARY_PATH=~/betaflight_gazebo/build:$LD_LIBRARY_PATH
gz sim -v4 -r ~/betaflight_gazebo/worlds/iris_runway_betaflight.sdf
```
Пока еще не разобрался в каком порядке
_____________________________________________________________________________________

start_motors пока в симуляции не отображается
_____________________________________________________________________________________
**Заметка:**
__________________________________________________________
**В CLI конфигуратора нужно выполнить эти команды:<br>**
1 - отключает моторы<br>
2 - разрешает арминг<br>
3 - Разрешает MSP  переопределять первые 4 канала -мvаска 15 в двоичной системе = 1111, что означает каналы: Roll, Pitch, Throttle, Yaw<br>
4 - СОхраняет фэйлсейф<br>
```bash
feature -MOTOR_STOP
set enable_stick_arming = ON
set msp_override_channels_mask = 15
set msp_override_failsafe = OFF
```
**Потом можно проверить это всё:**
# 
# Building AutoComplete Cache ... Done!
# 
# feature
Enabled:  AIRMODE ANTI_GRAVITY
Available:  INFLIGHT_ACC_CAL MOTOR_STOP 3D
Unavailable: RX_PPM RX_SERIAL SERVO_TILT SOFTSERIAL GPS OPTICALFLOW RANGEFINDER TELEMETRY RX_PARALLEL_PWM RSSI_ADC LED_STRIP DISPLAY OSD CHANNEL_FORWARDING TRANSPONDER RX_SPI ESC_SENSOR

# get enable_stick_arming
enable_stick_arming = ON
Allowed values: OFF, ON
Default value: OFF

# get msp_override_channels_mask
msp_override_channels_mask = 15
Allowed range: 0 - 262143
Default value: 0
