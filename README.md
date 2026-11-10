# NH₂ 라디칼 WSL 실습

[NH₂ 전체 실습 매뉴얼 (HWPX)](https://github.com/Skylark51/dft-tutorial-nh2-wsl/releases/download/v1.6.1/NH2-WSL-Manual.hwpx)

## 설치

Ubuntu WSL의 Bash에서 실행합니다. `curl`, Python 3, `vi`가 필요합니다.

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Skylark51/dft-tutorial-nh2-wsl/v1.6.1/install-dft-nh2.sh)
```

실습 디렉터리 이름을 입력합니다. Enter만 누르면 `nh2`를 사용합니다. 다시 열 때 같은 이름을 입력하면 이전 작업이 남아 있습니다. 인터넷 없이 다시 열 때는 `bash --rcfile ~/.local/share/dft-nh2/v1.6.1/activate -i`를 실행합니다.

실습 디렉터리에서 `ls`를 실행하면 NH₂의 시작 구조인 `nh2.xyz`가 보입니다. `cat nh2.xyz`로 좌표(Å)를 확인할 수 있습니다.

입력의 route, 원소 기호와 `%chk`·`%oldchk`는 대소문자를 섞어 쓸 수 있습니다. 체크포인트는 정확한 이름을 먼저 찾고, 일치하는 파일이 없으면 대소문자를 무시해 유일한 후보를 찾습니다. 셸에서 `g16 < 파일.inp`에 쓰는 파일명은 실제 이름과 일치해야 합니다.

## 1. Opt → Freq → BB

실습 셸에서 `ls`로 `nh2.xyz`를 확인합니다. Opt는 XYZ의 원소·좌표 세 줄만 사용합니다. XYZ의 첫 줄(원자 수)과 둘째 줄(설명)은 Gaussian 입력에 넣지 않습니다.

각 입력을 `vi 파일명.inp`에서 작성하고 마지막 줄 뒤에 빈 줄을 둡니다. Esc 후 `:wq`로 저장합니다. 실행 후 출력이 열리면 `/검색어`로 확인하고 `:q`로 닫습니다.

### 1A. Opt · Cartesian 좌표에서 구조 최적화

```text
%chk=nh2-opt.chk
%CPU=0-1
%mem=1GB
#p UB3LYP/def2SVP Opt Pop=Full

NH2 radical ground-state optimization

0 2
N     0.000000     0.000000     0.000000
H     0.000000     0.000000     1.030000
H     0.892006     0.000000    -0.515000

```

```bash
g16 < nh2-opt.inp > nh2-opt.out
```

검색어 `Optimization completed`. ²B₁ 최적화 에너지 −55.8309531917 Eh.

### 1B. Freq · Opt 체크포인트에서 진동수 계산

```text
%oldchk=nh2-opt.chk
%chk=nh2-opt-freq.chk
%CPU=0-1
%mem=1GB
#p UB3LYP/def2SVP Freq Pop=Full Geom=AllCheck Guess=Read

```

```bash
g16 < nh2-opt-freq.inp > nh2-opt-freq.out
```

검색어 `Frequencies --`. 1531.9485, 3324.1809, 3406.8390 cm⁻¹.

`Geom=Check` 형식도 사용할 수 있습니다. 이 형식은 route 뒤에 제목과 `0 2`를 적고, 좌표를 체크포인트에서 읽습니다.

```text
%chk=nh2-opt-freq.chk
%oldchk=nh2-opt.chk
%CPU=0-1
%mem=1GB
#p UB3LYP/def2SVP Freq Pop=Full Guess=Read Geom=Check

NH2

0 2

```


### 1C. BB · Freq 체크포인트에서 큰 기저 단일점 계산

```text
%oldchk=nh2-opt-freq.chk
%chk=nh2-opt-freq-bb.chk
%CPU=0-1
%mem=1GB
#p UB3LYP/def2TZVPP SP Geom=AllCheck Guess=Read

```

```bash
g16 < nh2-opt-freq-bb.inp > nh2-opt-freq-bb.out
```

검색어 `SCF Done`. 고정 구조에서 UB3LYP/def2TZVPP 에너지 −55.9064118524 Eh.

Freq는 Opt의 `Opt`를 `Freq`로 바꾸고 `Pop=Full`을 유지합니다. `Geom=AllCheck Guess=Read`와 `%oldchk`로 최적화된 구조와 파동함수를 읽으므로 제목·전하·다중도·좌표는 반복하지 않습니다. BB는 Freq의 체크포인트를 읽고 구조를 고정합니다. `BB`는 실습 파일명 접미사이며 Gaussian의 기본 계산이 단일점이므로 route에서 `SP`를 생략할 수 있습니다. `Pop=Full`을 추가하면 상세 오비탈 출력이 제공됩니다.

## 2. Read Only · BB 오비탈 점유 확인 (선택)

```text
%oldchk=nh2-opt-freq-bb.chk
%chk=nh2-opt-freq-bb-read.chk
%CPU=0-1
%mem=1GB
#p UB3LYP/def2TZVPP Geom=AllCheck Guess=(Read,Only) Pop=Full

```

```bash
g16 < nh2-opt-freq-bb-read.inp > nh2-opt-freq-bb-read.out
```

검색어 `Beta Molecular Orbital Coefficients`. β 4번 A₁은 점유(O), β 5번 B₁은 비점유(V)입니다.

## 3. Read Alter · β 4 ↔ 5 교환

BB에서 `Pop=Full`로 β 오비탈 번호를 확인했다면 Read Only 단계는 건너뛰고, Alter의 `%oldchk`에 BB 체크포인트를 바로 지정할 수 있습니다. Read Only를 실행한 경우 그 체크포인트도 사용할 수 있습니다. 입력·출력 파일명과 체크포인트의 접미사는 자유롭게 정합니다. 예를 들어 `nh2-opt-freq-bb-pop.chk`도 사용할 수 있으며, 다음 입력의 `%oldchk`에는 실제 저장한 이름을 적습니다.

```text
%oldchk=nh2-opt-freq-bb.chk
%chk=nh2-opt-freq-bb-alter.chk
%CPU=0-1
%mem=1GB
#p UB3LYP/def2TZVPP SP Geom=AllCheck Guess=(Read,Alter) Pop=Full


4 5

```

```bash
g16 < nh2-opt-freq-bb-alter.inp > nh2-opt-freq-bb-alter.out
```

검색어 `orbitals switched`와 `The electronic state is`. route 뒤의 연속된 빈 줄 두 개 중 둘째 줄은 α 섹션입니다. 교환 후 SCF는 ²A₁, β 점유는 A₁ A₁ B₂ B₁입니다.

## 4. Stable · 수렴한 파동함수 안정성 검사

```text
%oldchk=nh2-opt-freq-bb-alter.chk
%chk=nh2-opt-freq-bb-stable.chk
%CPU=0-1
%mem=1GB
#p UB3LYP/def2TZVPP Stable Geom=AllCheck Guess=Read Pop=Full

```

```bash
g16 < nh2-opt-freq-bb-stable.inp > nh2-opt-freq-bb-stable.out
```

검색어 `internal instability`. ²A₁ 점유는 유지됐고, 안정성 검사에서 음의 고윳값(−0.0754797)이 검출됐습니다. SCF가 수렴했다는 사실과 파동함수의 안정성은 별개입니다.

같은 구조와 def2TZVPP 기저에서 ²B₁ BB 에너지는 −55.9064118524 Eh, 교환 후 ²A₁ 에너지는 −55.8271904005 Eh입니다. 차이는 0.0792214519 Eh(2.1557 eV)입니다.

## 실습 셸에서 HOMO 보기

```bash
nh2-orbitals
```

- `1` · 교환 전 ²B₁의 β HOMO (4번 A₁)
- `2` · 교환 후 ²A₁의 β HOMO (4번 B₁)
- `3` / `4` · 교환 전후의 α HOMO (5번 B₁)
- `5` · 교환 후 ²A₁의 단일 점유 α A₁ (4번)
- 방향키 또는 `h j k l` · 회전. `r` · 시점 초기화. `q` · 실습 셸로 돌아가기.

라이온의 BB 및 Alter 체크포인트에서 `formchk`와 `cubegen`으로 생성한 자료를 등치값 ±0.02에서 표시합니다. 두 색은 오비탈 파동함수의 위상을 나타냅니다. 뷰어는 설치본의 참조 자료를 사용하므로 실습용 `.chk` 파일이나 추가 접속이 필요 없습니다.

## 별도 예제 · 기저별 오비탈 교환

각 파일을 `vi 파일명.inp`로 열어 입력을 작성합니다. `i`로 입력하고 Esc 후 `:wq`로 저장합니다. 완성 입력은 `~/.local/share/dft-nh2/v1.6.1/data/`의 `*.inp` 파일에 있습니다. 아래 파일명은 예시입니다.

| 단계 | def2SVP 예시 파일명 | Route에 추가할 항목 |
|---|---|---|
| 바닥상태 최적화 | `nh2-def2svp-opt.inp` | `Opt Pop=Full` |
| 교환 전 점유 확인 | `nh2-def2svp-read.inp` | `Geom=AllCheck Guess=(Read,Only)` |
| β 4 ↔ 5 교환 | `nh2-def2svp-swap.inp` | `Geom=AllCheck Guess=(Read,Only,Alter,Save)` |
| 고정 구조 단일점 SCF | `nh2-def2svp-scf.inp` | `Geom=AllCheck Guess=Read SP` |

모든 route는 `#p UB3LYP/def2SVP`로 시작합니다. 교환 전 확인, 교환, 단일점에는 `Pop=(Full,NBO) GFInput GFOldPrint`를 추가합니다. 최적화 입력은 `0 2`와 NH₂ Z-matrix를 사용합니다. `Geom=AllCheck` 단계는 제목, 전하·다중도, 구조를 체크포인트에서 읽습니다. 교환 입력은 route를 닫는 빈 줄 뒤에 α 섹션을 닫는 빈 줄을 더 두고, β 쌍 `4 5`와 마지막 빈 줄을 넣습니다.

`%chk`는 단계마다 별도로 지정합니다. 교환 전 확인과 교환의 `%oldchk`는 같은 기저의 최적화 체크포인트, 단일점의 `%oldchk`는 같은 기저의 교환 체크포인트입니다. 아래 명령을 한 줄씩 실행합니다.

```bash
g16 < nh2-def2svp-opt.inp > nh2-def2svp-opt.out
g16 < nh2-def2svp-read.inp > nh2-def2svp-read.out
g16 < nh2-def2svp-swap.inp > nh2-def2svp-swap.out
g16 < nh2-def2svp-scf.inp > nh2-def2svp-scf.out
```

검증이 통과하면 약 5초 뒤 출력이 `vi`에서 읽기 전용으로 열립니다. `/SCF Done`, `/orbitals switched`, `/The electronic state is`로 검색하고 `n`으로 다음 일치 항목에 이동합니다. `:q`로 닫으면 셸로 돌아갑니다. def2TZVPP도 같은 흐름으로, 독립된 체크포인트 이름과 `#p UB3LYP/def2TZVPP`를 사용합니다.

실습용 `g16`은 라이온의 참조 출력을 재생하고, 작업 순서를 확인하는 모의 `.chk` 파일을 생성합니다. 참조 로그에는 라이온의 원래 제목과 파일명이 표시되며 서버 계정, 호스트 이름과 스크래치 경로는 가렸습니다. 입력 오류 시 Bash의 `>`가 지정한 출력 파일을 비웁니다.

## 라이온 결과

기저마다 ²B₁을 최적화하고 그 구조에서 ²A₁ 단일점 SCF를 수렴시켰습니다. 두 기저에서 교환 후 β 점유가 `A1 A1 B2 B1`으로 유지됐고, α 5개·β 4개와 ⟨Sᶻ⟩ = +0.5는 교환 전후에 같았습니다.

| 기저 | E(²B₁), Eh | E(²A₁), Eh | ΔE, Eh | ΔE, eV | ²A₁ ⟨S²⟩ |
|---|---:|---:|---:|---:|---:|
| def2SVP | −55.8309531917 | −55.7511883925 | 0.0797647992 | 2.1705 | 0.7514 |
| def2TZVPP | −55.9066009369 | −55.8305237809 | 0.0760771560 | 2.0702 | 0.7524 |

ΔE = E(²A₁) − E(²B₁)입니다. 각 행의 두 에너지는 같은 기저와 해당 기저의 ²B₁ 최적화 구조에서 비교합니다. 교환 직후 `Guess=Only` 출력 대신 단일점의 `SCF Done`을 사용합니다.

배포 파일을 다시 만들려면 이 폴더에서 `python3 build_installer.py`를 실행합니다.
