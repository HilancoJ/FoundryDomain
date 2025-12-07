#!/usr/bin/env bash
# Minimal hwmon-based fan/pump controller (safe defaults).
# Runs as root. Tailor MIN/MAX and temp points as desired.

set -euo pipefail

# --- Configuration (safe defaults) ---
PUMP_MIN=60        # PWM (0-255) minimum for pump (≈23%)
PUMP_MAX=255       # PWM max for pump (100%)
PUMP_TEMP_LOW=25   # °C: coolant temp where pump stays at PUMP_MIN
PUMP_TEMP_HIGH=60  # °C: coolant temp where pump goes to PUMP_MAX

FAN_MIN=40         # PWM (0-255) min for radiator fans (≈15%)
FAN_MAX=255
FAN_TEMP_LOW=40    # °C: GPU/CPU temp where fans start ramping
FAN_TEMP_HIGH=85   # °C: temp where fans reach FAN_MAX

SLEEP_INTERVAL=5   # seconds between updates

# --- Helpers ---
clamp() {
  local val=$1 min=$2 max=$3
  if (( val < min )); then echo $min
  elif (( val > max )); then echo $max
  else echo $val
  fi
}

# Linear interpolation from (t0->v0) to (t1->v1)
interp_pwm() {
  local temp=$1 t0=$2 v0=$3 t1=$4 v1=$5
  if (( temp <= t0 )); then echo $v0; return; fi
  if (( temp >= t1 )); then echo $v1; return; fi
  # do integer math: v = v0 + (temp - t0) * (v1 - v0) / (t1 - t0)
  local num=$(( (temp - t0) * (v1 - v0) ))
  local den=$(( t1 - t0 ))
  local add=$(( num / den ))
  echo $(( v0 + add ))
}

# Find hwmon path by name
hwmon_by_name() {
  local wanted="$1"
  for d in /sys/class/hwmon/hwmon*; do
    [ -f "$d/name" ] || continue
    if grep -qFx "$wanted" "$d/name" 2>/dev/null; then
      echo "$d"
      return 0
    fi
  done
  return 1
}

# Read functions (millidegrees -> degrees integer)
read_temp_c() {
  local path="$1"  # full path to tempX_input
  if [ -r "$path" ]; then
    awk 'BEGIN{printf("%d\n", int($1/1000))}' "$path"
  else
    echo 0
  fi
}

# Write PWM safely
write_pwm() {
  local pwm_path="$1" value="$2"
  if [ -w "$pwm_path" ]; then
    printf "%d" "$value" > "$pwm_path"
  else
    echo "ERR: cannot write $pwm_path" >&2
  fi
}

# --- Discover hwmon paths ---
KR=$(hwmon_by_name "kraken2023" || true)
ASUS=$(hwmon_by_name "asus" || true)
CORE=$(hwmon_by_name "coretemp" || true)
NV=$(hwmon_by_name "nvidia" || true)  # may not exist until GPU active

# Map expected files (adjust if names differ)
PUMP_TEMP=""
PUMP_PWM=""
PUMP_PWM_ENABLE=""
FAN_PWM=""
FAN_PWM_ENABLE=""
CPU_TEMP=""
GPU_TEMP=""

if [ -n "$KR" ]; then
  # common names observed: temp1_input -> coolant, pwm1 -> pump, pwm2 -> fan
  PUMP_TEMP="$KR/temp1_input"
  PUMP_PWM="$KR/pwm1"
  PUMP_PWM_ENABLE="$KR/pwm1_enable"
  FAN_PWM="$KR/pwm2"
  FAN_PWM_ENABLE="$KR/pwm2_enable"
fi

if [ -n "$CORE" ]; then
  CPU_TEMP="$CORE/temp1_input"
fi

if [ -n "$NV" ]; then
  GPU_TEMP="$NV/temp1_input"
fi

# If NV hwmon not present, fallback to nvidia-smi (if available)
read_gpu_temp() {
  if [ -n "$GPU_TEMP" ] && [ -r "$GPU_TEMP" ]; then
    read_temp_c "$GPU_TEMP"
  else
    # fallback to nvidia-smi if installed
    if command -v nvidia-smi >/dev/null 2>&1; then
      nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits 2>/dev/null | head -n1 | awk '{print int($1)}'
    else
      echo 0
    fi
  fi
}

# Enable manual PWM if disabled
enable_manual_pwm() {
  for p in "$PUMP_PWM_ENABLE" "$FAN_PWM_ENABLE"; do
    [ -z "$p" ] && continue
    if [ -w "$p" ]; then
      printf "%d" 1 > "$p" || true
    fi
  done
}

# --- Main loop ---
echo "Starting hwmon fancurve loop..."
enable_manual_pwm

while true; do
  # read temps (in °C integers)
  cooltemp=0; cputemp=0; gputemp=0
  if [ -n "$PUMP_TEMP" ] && [ -r "$PUMP_TEMP" ]; then
    cooltemp=$(read_temp_c "$PUMP_TEMP")
  fi
  if [ -n "$CPU_TEMP" ] && [ -r "$CPU_TEMP" ]; then
    cputemp=$(read_temp_c "$CPU_TEMP")
  fi
  gputemp=$(read_gpu_temp)

  # choose control temps
  control_temp=$(( cputemp > gputemp ? cputemp : gputemp ))

  # compute pump PWM from coolant temp
  pump_pwm=$(interp_pwm "$cooltemp" "$PUMP_TEMP_LOW" "$PUMP_MIN" "$PUMP_TEMP_HIGH" "$PUMP_MAX")
  pump_pwm=$(clamp "$pump_pwm" "$PUMP_MIN" "$PUMP_MAX")

  # compute fan PWM from max(CPU,GPU)
  fan_pwm=$(interp_pwm "$control_temp" "$FAN_TEMP_LOW" "$FAN_MIN" "$FAN_TEMP_HIGH" "$FAN_MAX")
  fan_pwm=$(clamp "$fan_pwm" "$FAN_MIN" "$FAN_MAX")

  # apply (convert to ints)
  if [ -n "$PUMP_PWM" ]; then
    write_pwm "$PUMP_PWM" "$pump_pwm"
  fi
  if [ -n "$FAN_PWM" ]; then
    write_pwm "$FAN_PWM" "$fan_pwm"
  fi

  # a tiny heartbeat logging (optional)
  echo "$(date +%F\ %T) cool:${cooltemp}C cpu:${cputemp}C gpu:${gputemp}C pumpPWM:${pump_pwm} fanPWM:${fan_pwm}"

  sleep "$SLEEP_INTERVAL"
done