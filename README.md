# NH₂ 오비탈 교환 WSL 실습

## 설치

Ubuntu WSL의 Bash에서 실행합니다. Python 3과 `vi`가 필요합니다. 설치 파일은 사용자 홈에 실습 도구와 참조 데이터를 풀어 놓습니다. 관리자 권한이나 라이온 계정은 필요 없습니다.

GitHub에서 설치 파일을 내려받고 실습 셸을 여는 명령입니다.

```bash
curl -fL https://github.com/Skylark51/dft-tutorial-nh2-wsl/releases/download/v1.0.0/install-dft-nh2.sh -o install-dft-nh2.sh && bash install-dft-nh2.sh && bash --rcfile ~/.local/share/dft-nh2/activate -i
```

같은 실습을 다시 열 때는 `bash --rcfile ~/.local/share/dft-nh2/activate -i`만 실행합니다. 실습 셸은 `exit`로 닫습니다.

## 실습

```bash
mkdir -p ~/nh2-lesson
cd ~/nh2-lesson
vi A.inp
g16 < A.inp > A.out
less A.out
```

1. 먼저 `#p UHF/6-31G(d) Guess=Only` 입력을 작성합니다. `0 2`와 NH₂ Z-matrix를 사용합니다. N–H 거리는 1.03 Å, H–N–H 각은 120.0°입니다. 출력에서 초기 상태와 β 점유 오비탈을 확인합니다.
2. `vi B.inp`에서 `#p UHF/6-31G(d) Opt Guess=Alter`를 작성합니다. 변수 블록을 끝내는 빈 줄 뒤에 **α 교환 섹션을 닫는 빈 줄을 한 줄 더** 넣습니다. 다음 줄에 β 교환 쌍 `4 5`를 쓰고 빈 줄로 닫습니다.
3. `g16 < B.inp > B.out`을 실행하고 `grep -A1 'orbitals switched' B.out`로 교환을 확인합니다. `grep -E 'electronic state|Optimization completed|Normal termination' B.out`로 상태와 종료를 확인합니다.

완성 입력은 `~/.local/share/dft-nh2/data/nh2-guess.inp`와 `nh2-alter.inp`에서 확인할 수 있습니다. 검사기는 이 두 실습의 route, 전하·다중도, Z-matrix와 변수 값, 교환 섹션을 확인합니다. 파일명과 제목은 자유롭게 정할 수 있습니다. 오류는 터미널에 표시되고 종료 코드는 1입니다. `>`는 Bash가 처리하므로 오류가 나도 대상 파일이 비워집니다.

## 라이온 기준 결과

Gaussian 16으로 실행한 두 작업 모두 정상 종료했습니다. 기본 초기 추정의 β 점유 대칭은 `A1 A1 B2 A1`이며, 교환 직후에는 `A1 A1 B2 B1`입니다. α 점유는 그대로 유지됩니다. 초기 상태는 ²B₁에서 ²A₁로 바뀌며, `Opt Guess=Alter`는 최종 ²A₁ 상태와 UHF 에너지 −55.5015891139 Hartree에서 최적화를 마쳤습니다. 수업에서 재현하는 계산 수준은 Gaussian의 NH₂ 예제에 맞춘 UHF/6-31G(d)입니다. [Gaussian 사용 설명서의 Guess 예제](https://tungsten.ch.uj.edu.pl/doc/g09doc/g09ur/k_guess.htm)

실습용 `g16`은 검증이 통과하면 미리 계산한 참조 출력을 그대로 표준 출력에 씁니다. 따라서 출력에 보이는 제목, 자원 설정, 체크포인트 이름은 라이온 참조 계산의 것입니다. 참조 출력에서 서버 계정, 호스트 이름과 스크래치 경로를 가렸습니다. 학생 측에서 계산, 체크포인트 생성, 네트워크 접속은 발생하지 않습니다.

배포 파일을 다시 만들려면 이 폴더에서 `python3 build_installer.py`를 실행합니다.
