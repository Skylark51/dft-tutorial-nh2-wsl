# NH₂ 오비탈 교환 WSL 실습

## 설치

Ubuntu WSL의 Bash에서 실행합니다. `curl`, Python 3, `vi`가 필요합니다. 관리자 권한이나 라이온 계정은 필요 없습니다.

GitHub에서 설치 파일을 내려받고 실습 셸을 여는 명령입니다.

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Skylark51/dft-tutorial-nh2-wsl/v1.2.0/install-dft-nh2.sh)
```

셸이 열리면 실습 디렉터리 이름을 입력합니다. Enter만 누르면 `nh2`를 사용합니다. 파일은 WSL 홈 아래 `~/.local/share/dft-nh2/workspaces/`에 저장됩니다. 다시 열 때 같은 이름을 입력하면 이어서 실습할 수 있습니다.

인터넷 없이 다시 열 때는 `bash --rcfile ~/.local/share/dft-nh2/v1.2.0/activate -i`를 실행합니다. 실습 셸은 `exit`로 닫습니다.

## 실습

```bash
vi nh2-swap.inp
g16 < nh2-swap.inp > nh2-swap.out
```

파일명은 예시입니다. `vi`에서 `i`를 눌러 입력을 작성하고, `Esc` 후 `:wq`로 저장합니다. 같은 `vi` 명령으로 입력을 다시 열 수 있습니다. 기본 초기 추정의 route는 `#p UHF/6-31G(d) Guess=Only`입니다. 교환 실습에는 `#p UHF/6-31G(d) Opt Guess=Alter`를 사용합니다. 두 입력 모두 전하와 다중도는 `0 2`입니다. 교환 입력에서는 변수 블록 뒤에 **α 교환 섹션을 닫는 빈 줄**을 한 줄 더 두고, β 교환 쌍 `4 5`를 입력한 뒤 빈 줄로 닫습니다.

입력이 맞으면 약 5초 뒤 완료 메시지가 표시되고, 지정한 출력 파일이 `vi`에서 읽기 전용으로 열립니다. `/orbitals switched` 또는 `/Optimization completed`를 입력하고 Enter를 누르면 해당 줄로 이동합니다. `:q`로 닫으면 셸로 돌아갑니다. 출력은 `vi nh2-swap.out`으로도 다시 열 수 있습니다.

완성 입력은 `~/.local/share/dft-nh2/v1.2.0/data/`에서 확인할 수 있습니다. 입력이 틀리면 터미널에 오류가 표시됩니다. `>`는 Bash가 처리하므로 입력 오류가 나도 대상 출력 파일은 비워집니다.

## 라이온 기준 결과

Gaussian 16으로 실행한 두 작업 모두 정상 종료했습니다. 기본 초기 추정의 β 점유 대칭은 `A1 A1 B2 A1`이며, 교환 직후에는 `A1 A1 B2 B1`입니다. α 점유는 그대로 유지됩니다. 초기 상태는 ²B₁에서 ²A₁로 바뀌며, `Opt Guess=Alter`는 최종 ²A₁ 상태와 UHF 에너지 −55.5015891139 Hartree에서 최적화를 마쳤습니다. 수업에서 재현하는 계산 수준은 Gaussian의 NH₂ 예제에 맞춘 UHF/6-31G(d)입니다. [Gaussian 사용 설명서의 Guess 예제](https://tungsten.ch.uj.edu.pl/doc/g09doc/g09ur/k_guess.htm)

실습용 `g16`은 검증이 통과하면 미리 계산한 참조 출력을 그대로 표준 출력에 씁니다. 따라서 출력에 보이는 제목, 자원 설정, 체크포인트 이름은 라이온 참조 계산의 것입니다. 참조 출력에서 서버 계정, 호스트 이름과 스크래치 경로를 가렸습니다. 학생 측에서 계산, 체크포인트 생성, 네트워크 접속은 발생하지 않습니다.

배포 파일을 다시 만들려면 이 폴더에서 `python3 build_installer.py`를 실행합니다.
