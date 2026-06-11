---
layout: podcast
arxiv_id: "manual-2026-06-11-visualtactile-fusion-for-transparent-obj"
title: "Visual-tactile Fusion for Transparent Object Grasping in Complex Backgrounds"
authors: "Shoujie Li, Haixin Yu, Wenbo Ding et al."
published_date: 2023-06-06
permalink: /podcasts/manual-2026-06-11-visualtactile-fusion-for-transparent-obj/
---

<audio controls style="width:100%;margin-bottom:2em;">
  <source src="/research_pipeline/assets/audio/manual-2026-06-11-visualtactile-fusion-for-transparent-obj.mp3" type="audio/mpeg">
  Your browser does not support audio.
</audio>

## Paper

**Visual-tactile Fusion for Transparent Object Grasping in Complex Backgrounds** — Shoujie Li, Haixin Yu, Wenbo Ding et al.

## Summary Card

### Motivation
Transparent objects are notoriously difficult for robots to grasp due to their visual transparency and reflectivity, which confound standard depth sensors and detection algorithms. This is especially problematic in complex backgrounds and varying lighting conditions, limiting robotic manipulation in real-world applications like logistics and service robotics.

### Method
The paper proposes a visual-tactile fusion framework that integrates a novel grasping network (TGCNN) for detection, a fully convolutional network for tactile feature extraction, and a central location based adaptive grasping strategy inspired by human grasping. A key innovation is the multi-scene synthetic dataset with Gaussian-distributed annotations, and a fusion method that combines vision and touch to classify and grasp transparent objects, improving robustness against visual ambiguities.

### Key Results
The tactile calibration improved grasping success rate by 36.7% over direct grasping, and the visual-tactile fusion for classification boosted accuracy by 34%. TGCNN demonstrated strong performance in both synthetic and real scenes, showing effective transfer from simulation to reality.

### Takeaways
This work demonstrates that combining vision and tactile sensing can significantly overcome the limitations of each modality alone for transparent objects, offering a practical pathway for robust robotic grasping in cluttered, real-world environments. The synthetic dataset generation and fusion strategy may serve as a template for other challenging perception tasks.

[Back to paper page](/research_pipeline/papers/manual-2026-06-11-visualtactile-fusion-for-transparent-obj/)
