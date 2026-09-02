<div align="center">

![header](https://capsule-render.vercel.app/api?type=soft&color=0:0D1B2A,100:1B98E0&height=200&section=header&text=Mingi%20Kim&fontSize=44&fontColor=ffffff&fontAlignY=38&desc=Humanoid%20Whole-Body%20Control%20%C2%B7%20Physical%20AI%20%C2%B7%20Robot%20Learning&descSize=15&descAlignY=58&descColor=cfe8ff&animation=fadeIn)

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=18&duration=3200&pause=900&color=1B98E0&center=true&vCenter=true&width=560&lines=Whole-Body+Control+for+Humanoid+Robots;Physical+AI+%C3%97+Model-based+Control;From+simulation+to+the+real+robot)](https://github.com/Mingi1211)

</div>

---

## ▍01 · about me

Undergraduate researcher at **DREAM Lab**, School of Robotics, **Kwangwoon University**.

I got here through **learning-based manipulation** — putting a VLA model on a real arm and making it
actually move. What I want to build next is bigger than a gripper: **whole-body motion for humanoid robots**.

|  |  |
| :-- | :-- |
| 🔬 **Lab** | DREAM Lab · School of Robotics, Kwangwoon University |
| 🎯 **Goal** | Whole-body control (WBC) for humanoid robots |
| 🧠 **Approach** | Model-based control **×** learned policies — not either one alone |
| 🛰 **Env** | Ubuntu 24.04 · VS Code Remote-SSH · A100 remote training |

---

## ▍02 · research focus

```yaml
primary:
  - Whole-Body Control (WBC) for humanoid robots
  - Full-body motion, balance and contact scheduling

physical_ai:
  - Vision-Language-Action (VLA) policies on real hardware
  - Imitation learning, dataset design, sim-to-real gaps

what_i_actually_care_about: >
  A learned policy is only useful if it respects the dynamics
  and the constraints of a real body. I want to sit exactly on
  that boundary — where the model meets the controller.
```

---

## ▍03 · tech stack

**Robot Learning & Simulation**

![MuJoCo](https://img.shields.io/badge/MuJoCo-1B98E0?style=for-the-badge&logoColor=white)
![OpenVLA](https://img.shields.io/badge/OpenVLA-0D1B2A?style=for-the-badge&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![HuggingFace](https://img.shields.io/badge/Hugging_Face-FFB000?style=for-the-badge&logo=huggingface&logoColor=333)
![TFDS](https://img.shields.io/badge/RLDS_%2F_TFDS-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)

**Languages & Numerics**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-4D77CF?style=for-the-badge&logo=numpy&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logoColor=white)

**Environment & Tooling**

![Linux](https://img.shields.io/badge/Ubuntu_24.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge&logo=uv&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![VSCode](https://img.shields.io/badge/Remote--SSH-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)

---

## ▍04 · featured project

### 🦝 OpenVLA × RaccoonBot — making a 7-D policy drive a 4-DoF arm

<p>
  <img src="https://img.shields.io/badge/OpenVLA-0D1B2A?style=flat-square"/>
  <img src="https://img.shields.io/badge/MuJoCo-1B98E0?style=flat-square"/>
  <img src="https://img.shields.io/badge/LoRA-FFB000?style=flat-square&logoColor=333"/>
  <img src="https://img.shields.io/badge/RLDS_%2F_TFDS-FF6F00?style=flat-square"/>
  <img src="https://img.shields.io/badge/Real_Hardware-2E9E4F?style=flat-square"/>
</p>

**The problem.** OpenVLA emits a 7-D action `[dx, dy, dz, droll, dpitch, dyaw, gripper]`, but RaccoonBot is
effectively a **4-DoF** arm. With the baseline client the gripper command stayed near zero — the arm would
reach the target and then simply never close.

**What I did.**

- **Dataset extension** — 20 MuJoCo episodes (18 train / 2 val), `grasp` + `push` tasks, cylinder / cube / sphere
  objects, 14 unique language instructions
- **Pipeline rebuild** — RLDS → TFDS conversion, then a 100-step LoRA run to verify the dataset loads and
  checkpoints survive the round trip
- **Staged action mapping** — kept OpenVLA in the loop, but reshaped its output into a stage machine:
  `approach → descend → close → lift` for grasp/lift, `approach → descend → push` for push
- **Inference budgeting** — `--request_every_n_steps` so the policy is queried on a schedule instead of every step
- **Full instrumentation** — raw vs. assisted action, inference latency, motion time, gripper command and lift
  distance logged to CSV for every step, so failures were diagnosable instead of anecdotal

**Results.**

| | baseline | after |
| :-- | :-- | :-- |
| Cylinder grasp-and-lift · MuJoCo | ❌ never closes | ✅ **0.0162 m** / **0.0159 m** |
| Server requests per 28-step episode | 28 | **10** |
| Mean step time | 811.7 ms | **581.2 ms** |
| Grasp-and-lift on the **real** RaccoonBot | — | ✅ **0.0122 m** |

Generalization to unseen objects and tasks: `blue cube lift` ✅ 0.0120 m · `green sphere push` ✅ 0.0104 m.

➜ **[Mingi1211/PhysicalAI_Assignment_2024405002](https://github.com/Mingi1211/PhysicalAI_Assignment_2024405002)**

---

## ▍05 · now

```
[x]  VLA policy running end-to-end on real hardware
[ ]  Whole-body control formulations — task-priority & QP-based stacks
[ ]  Humanoid balance / full-body motion reproduction in MuJoCo
[ ]  The open question: can a learned policy be projected onto a WBC stack
     without throwing away its constraints?
```

---

## ▍06 · stats

<div align="center">

![stats](https://github-readme-stats.vercel.app/api?username=Mingi1211&show_icons=true&hide_border=true&title_color=1B98E0&icon_color=1B98E0&include_all_commits=true)
![langs](https://github-readme-stats.vercel.app/api/top-langs/?username=Mingi1211&layout=compact&hide_border=true&title_color=1B98E0&langs_count=6)

</div>

---

![footer](https://capsule-render.vercel.app/api?type=soft&color=0:1B98E0,100:0D1B2A&height=110&section=footer)
