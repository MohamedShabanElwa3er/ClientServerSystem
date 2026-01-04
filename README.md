# ✅ ClientServerSystem

![CI](https://github.com/<USERNAME>/<REPO>/actions/workflows/ci.yml/badge.svg)
![Qt](https://img.shields.io/badge/Qt-6-green)
![C++](https://img.shields.io/badge/C++-17-blue)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)
![Coverage](https://img.shields.io/badge/Coverage-gcov%2Flcov-blue)

---

## 👤 Author

- **Name:** Mohamed Waaer  
- **Email:** mohamed.waer@coretech-innovations.com  

---

## 📌 Project Overview

**ClientServerSystem** is a Qt 6–based C++ client–server application designed with a
modular architecture and full Continuous Integration (CI) support.

The project demonstrates:
- Modern C++ (C++17)
- Qt 6 development
- Client–server architecture
- Automated builds and testing
- Code coverage reporting
- Professional CI/CD practices

---

## 🏗 Project Structure
ClientServerSystem/
├── common/ # Shared logic and utilities
├── server/ # Server implementation
├── client/ # Client application
├── tests/
│ ├── qt/ # QtTest unit tests
│ └── gtest/ # GoogleTest unit tests
├── .github/
│ └── workflows/ # CI configuration
└── README.md

---

## 🔁 Continuous Integration (CI)

- **Platform:** GitHub Actions
- **OS:** Ubuntu (latest)
- **Compiler:** GNU g++ (C++17)
- **Qt Version:** Qt 6
- **Build Tool:** qmake
- **Test Frameworks:** QtTest, GoogleTest
- **Coverage Tools:** gcov, lcov

### CI Capabilities

✅ Clean builds  
✅ Headless Qt execution  
✅ QtTest & GoogleTest automation  
✅ Test source validation (fail‑fast)  
✅ Coverage generation (HTML)  
✅ Deliverable ZIP artifact  

---

## 🧪 Testing

### Qt Tests
- `test_parser`
- `test_append`
- `test_info`
- `test_cpu`

### GoogleTests
- `test_commands`

All tests are executed automatically on every push and pull request.

---

## 📊 Test Coverage

Code coverage is generated using **gcov + lcov** and published as an **HTML report**
(downloadable from CI artifacts).

Coverage includes:
- Common library
- Server command handlers
- Core logic

---

## 📦 CI Artifacts

Each CI run produces:
- ✅ Coverage report (HTML)
- ✅ CI summary report
- ✅ Deliverable ZIP package

---

## ✅ Status

✔ Build successful  
✔ All tests passed  
✔ Coverage generated  
✔ CI pipeline stable and reproducible  

---

## 📜 License

This project is provided for educational and professional demonstration purposes.

---

**Author:** Mohamed Waaer  
**Email:** mohamed.waer@coretech-innovations.com