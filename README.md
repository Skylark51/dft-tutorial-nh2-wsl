# NH₂ 오비탈 교환 WSL 실습

[학생용 실습 매뉴얼 (HWPX)](https://github.com/Skylark51/dft-tutorial-nh2-wsl/releases/download/v1.3.0/NH2-WSL-Manual.hwpx)

## 설치

Ubuntu WSL의 Bash에서 실행합니다. `curl`, Python 3, `vi`가 필요합니다.

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Skylark51/dft-tutorial-nh2-wsl/v1.3.0/install-dft-nh2.sh)
```

실습 디렉터리 이름을 입력합니다. Enter만 누르면 `nh2`를 사용합니다. 다시 열 때 같은 이름을 입력하면 이전 작업이 남아 있습니다. 인터넷 없이 다시 열 때는 `bash --rcfile ~/.local/share/dft-nh2/v1.3.0/activate -i`를 실행합니다.

## 실습

각 파일을 `vi 파일명.inp`로 열어 입력을 작성합니다. `i`로 입력하고 Esc 후 `:wq`로 저장합니다. 완성 입력은 `~/.local/share/dft-nh2/v1.3.0/data/`의 `*.inp` 파일에 있습니다. 아래 파일명은 예시입니다.

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
