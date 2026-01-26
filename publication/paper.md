---
title: "EZInput: A Cross-Environment Python Library for Easy UI Generation in Scientific Computing"
tags:
  - User Interface
  - Python
  - Jupyter Notebook
  - Terminal User Interface
  - Scientific Computing
authors:
  - name: "Bruno M. Saraiva"
    affiliations: [1]
    corresponding_author: true
    orcid: 0000-0002-9151-5477
  - name: "Iván Hidalgo-Cenalmor"
    affiliations: [3]
    orcid: 0009-0000-8923-568X
  - name: "António D. Brito"
    affiliations: [1]
    orcid: 0009-0001-1769-2627
  - name: "Damián Martínez"
    affiliations: [1]
    orcid: 0000-0002-5906-598X
  - name: "Tayla Shakespeare"
    affiliations: [1]
    orcid: 0000-0002-4159-0460
  - name: "Guillaume Jaquemet"
    affiliations: [3,4,5,6]
    corresponding_author: true
    orcid: 0000-0002-9286-920X
  - name: "Ricardo Henriques"
    affiliations: [1,2]
    corresponding_author: true
    orcid: 0000-0002-2043-5234
affiliations:
  - index: 1
    name: "Instituto de Tecnologia Química e Biológica António Xavier, Universidade Nova de Lisboa"
    location: "Oeiras, Portugal"
  - index: 2
    name: "UCL Laboratory for Molecular Cell Biology, University College London"
    location: "London, United Kingdom"
  - index: 3
    name: "Faculty of Science and Engineering, Cell Biology, Åbo Akademi University"
    location: "Turku, Finland"
  - index: 4
    name: "InFLAMES Research Flagship Center, University of Turku"
    location: "Turku, Finland"
  - index: 5
    name: "Turku Bioscience Centre, University of Turku and Åbo Akademi University"
    location: "Turku, Finland"
  - index: 6
    name: "Foundation for the Finnish Cancer Institute"
    location: "Helsinki, Finland"
date: 2026-01-22
bibliography: paper.bib
---

## Summary

Researchers face a persistent barrier when applying computational algorithms with parameter configuration typically demanding programming skills, interfaces differing across environments, and settings rarely persisting between sessions. This fragmentation forces repetitive input, slows iterative exploration, and undermines reproducibility because parameter choices are difficult to record, share, and reuse.
We present EZInput, a cross-runtime environment Python library enabling algorithm developers to automatically generate graphical user interfaces that make their computational tools accessible to end-users without programming expertise. EZInput employs a declarative specification system where developers define input requirements and validation constraints once; the library then handles environment detection, interface rendering, parameter validation, and session persistence across Jupyter notebooks, Google Colab, and terminal environments. This "write once, run anywhere" architecture enables researchers to prototype in notebooks and deploy identical parameter configurations for batch execution on remote systems without code changes or manual transcription. Parameter persistence, inspired by ImageJ/FIJI and adapted to Python workflows, saves and restores user configurations via lightweight YAML files, eliminating redundant input and producing shareable records that enhance reproducibility. EZInput supports diverse input types essential for scientific computing and it also includes built-in validation that ensures data integrity and clear feedback that reduces user friction.

---

## Statement of need

Computational methods are central to modern scientific research, yet their practical adoption is often limited by usability and reproducibility challenges. Algorithm developers typically prioritise scientific correctness and performance, while the creation of robust user interfaces is time-consuming, environment-dependent, and difficult to maintain. As a result, many tools require users to configure parameters directly in code, excluding non-programmers and making parameter choices difficult to document, share, and reuse.

Existing solutions address this problem only partially. Standalone graphical applications such as CellProfiler [@mcquin2018cellprofiler] and Orange [@demsar2013orange] provide accessible interfaces but require substantial development effort, constrain workflows, and usually target a single execution environment. Notebook-based approaches using Jupyter [@kluyver2016jupyter] enable interactive exploration but still rely on code edits for parameter configuration and lack persistent parameter memory, forcing repetitive input across sessions.

EZInput is designed to solve these problems for **scientifically focused algorithm developers** who want to make their tools accessible to **end-users without programming expertise**, while also supporting **reproducible, systematic parameter exploration**. By providing environment-agnostic interface generation and automatic parameter persistence, EZInput enables the same parameter configurations to be used consistently across interactive notebooks, cloud platforms, and terminal-based execution.

---

## State of the field

While powerful algorithms are being created, their adoption by non-programming users has been hampered by interfaces demanding programmatic expertise, creating a dichotomy between algorithm development and practical application. Recent community efforts have begun addressing this challenge, with notable successes in specific domains such as ZeroCostDL4Mic and DL4MicEverywhere for deep learning in microscopy [@von2021democratising; @DL4MicEverywhere] and napari for interactive image visualisation [@sofroniew2025napari]. However, these solutions typically target specific computational environments or application domains. What remains missing is a framework enabling developers to write interface specifications once and deploy them anywhere at the same time as it automatically maintains parameter configurations that enhance reproducibility and facilitate systematic testing across different parameter combinations.

Traditional approaches to bridging this accessibility gap have typically followed two distinct paths, each with inherent limitations. The first involves developing bespoke graphical user interfaces (GUIs) for individual algorithms, exemplified by tools such as CellProfiler for bioimage analysis [@mcquin2018cellprofiler] and Orange for data mining [@demsar2013orange]. Although these provide accessible entry points for non-programmers, they require substantial additional development effort, create fragmented user experiences across tools, and often constrain users to predefined workflows that limit algorithmic flexibility. Critically, such bespoke solutions typically target a single computational environment, preventing developers from easily distributing their tools to users working in different contexts. The second approach utilises notebook environments such as Jupyter [@kluyver2016jupyter], which offer more accessible entry points and have become the de facto standard for exploratory data analysis. However, notebook-based approaches still necessitate direct code manipulation for parameter configuration and critically lack persistent parameter settings essential for iterative workflows. This absence of parameter memory forces users to repeatedly input configurations across sessions, diminishing productivity in exploratory research contexts where rapid iteration over parameter spaces is fundamental, and making systematic testing across parameter combinations unnecessarily cumbersome.

ImageJ and its distribution FIJI have demonstrated the value of parameter persistence through their parameter memory systems, which automatically retain user settings across sessions, enabling rapid experimental iterations that significantly enhance productivity in image analysis pipelines [@imagej; @schindelin2012fiji]. This functionality has proven particularly valuable in microscopy workflows, where researchers frequently fine-tune processing parameters across diverse datasets. However, translating this functionality to the Python ecosystem has proven challenging due to architectural differences in development frameworks and the absence of a unified parameter management system that operates consistently across computational environments. Existing Python GUI frameworks such as ipywidgets provide building blocks for notebook interfaces but cannot be easily deployed elsewhere as they were developed with only jupyter notebooks in mind.

Here, we present EZInput, a cross-runtime environment Python library that bridges this accessibility gap by enabling algorithm developers to create user-friendly interfaces with minimal effort, making their tools accessible to end-users without programming expertise across diverse computational environments. The framework employs a declarative specification system where developers define input requirements and constraints once, after which EZInput automatically manages interface rendering, validation, and parameter persistence across Jupyter notebooks, Google Colab, and terminal environments \autoref{@fig:diagram}. This "write once, run anywhere" architecture eliminates the need for parallel development of multiple interfaces while maintaining full feature parity across environments. EZInput adapts ImageJ/FIJI's parameter memory concept to modern Python workflows through lightweight configuration files that automatically save and restore user settings across sessions, enabling the rapid iteration essential for exploratory data analysis. Unlike previous solutions that sacrifice either accessibility or algorithmic sophistication, EZInput preserves both through an architecture that separates interface concerns from computational logic, allowing algorithm developers to focus on their scientific domain as the library handles all aspects of user interaction, validation, and parameter management.

![**EZInput enables seamless cross-application user interfaces through unified declarative specifications.** The framework demonstrates consistent interface generation across computational environments without requiring environment-specific code modifications. Underlying Python code demonstrating the declarative specification system that generates both interfaces. A single parameter definition block specifies labels and inputs, with EZInput automatically handling environment detection and appropriate interface rendering. This "write once, run anywhere" approach eliminates the need for parallel development of multiple interfaces whilst maintaining full feature parity across environments. Parameter persistence functionality ensures that user configurations remain consistent between Jupyter and terminal environments, enabling seamless transitions between interactive exploration and production workflows. \label{fig:diagram}](ezinput_flow.png){ width=50% }

---

## Software Design

EZInput implements a declarative parameter specification system that fundamentally separates interface content definition from presentation logic \autoref{@fig:cross-application}. Developers specify input requirements through a simple, intuitive API where each parameter is defined by its type (integer range, float range, text input, file path, dropdown selection, checkbox), label, constraints (minimum/maximum values, valid options, file extensions), and optional default values. The library's core architecture automatically detects the execution environment and renders appropriate interface elements without requiring environment-specific code from developers. This automatic environment detection mechanism examines the Python runtime context, checking for the presence of IPython kernel connections and interactive shell characteristics to determine the optimal rendering backend.

![**EZInput enables seamless cross-application user interfaces through unified declarative specifications.** The framework demonstrates consistent interface generation across computational environments without requiring environment-specific code modifications. Underlying Python code demonstrating the declarative specification system that generates both interfaces. A single parameter definition block specifies labels and inputs, with EZInput automatically handling environment detection and appropriate interface rendering. This "write once, run anywhere" approach eliminates the need for parallel development of multiple interfaces whilst maintaining full feature parity across environments. Parameter persistence functionality ensures that user configurations remain consistent between Jupyter and terminal environments, enabling seamless transitions between interactive exploration and production workflows. \label{fig:cross-application}](code_example.png){ width=50% }

In Jupyter notebook environments, including Google Colab [@colab], EZInput leverages the ipywidgets library to generate interactive graphical controls that integrate seamlessly with the notebook interface. Numerical parameters are rendered as sliders with real-time value display, dropdown selections appear as native select widgets, text inputs provide inline editing with validation feedback, and file path inputs offer interactive file browser integration. The generated interfaces maintain full compatibility with Jupyter's output cell system, displaying parameter configurations inline with code cells and preserving interactive state across notebook sessions.

For terminal environments, EZInput employs promp\_toolkit to construct sophisticated text-based user interfaces (TUIs) that provide keyboard-navigable parameter configuration without graphical display requirements [@prompt_toolkit]. The terminal interface implements identical functionality to the Jupyter version, including parameter validation, constraint enforcement, help text display, and configuration persistence, ensuring consistent user experience regardless of computational context. Parameters are presented in a vertically scrollable list with clear visual hierarchy, keyboard shortcuts enable rapid navigation between fields, and validation feedback appears inline as users modify values. This terminal compatibility proves particularly valuable in high-performance computing environments and remote server contexts where graphical displays are limited but user-friendly parameter configuration remains essential.

A defining innovation of EZInput is its automatic parameter persistence system, which saves user configurations to lightweight YAML files stored alongside Python scripts or in user-specified locations. This functionality adapts ImageJ/FIJI's parameter memory concept to modern Python workflows, addressing a critical gap in existing notebook-based scientific computing tools. When users configure parameters through either Jupyter or terminal interfaces, EZInput automatically serializes their selections to a human-readable YAML file using a naming convention derived from the interface title. Upon subsequent executions, the library automatically detects and loads these configuration files, pre-populating interface elements with previously saved values. This eliminates the redundant parameter input that typically characterizes exploratory research workflows, where scientists iteratively refine analysis parameters across multiple sessions.

The parameter persistence mechanism implements selective memory through a flag on individual parameters, allowing developers to specify which parameters should persist across sessions and which should reset to defaults. This granular control proves essential for workflows where certain parameters (such as file paths or experimental conditions) vary between runs while others (such as algorithmic hyperparameters or processing settings) typically remain constant. Configuration files employ a structured YAML format that maintains parameter names, values, and metadata, ensuring robustness to parameter additions or removals across code versions. The human-readable format also enables manual editing of configuration files when programmatic parameter adjustment is desired, and supports version control integration for collaborative research contexts where parameter configurations constitute part of the experimental methods.

Beyond individual workflow efficiency, parameter persistence substantially enhances reproducibility in computational research. Configuration files generated by EZInput can be shared alongside datasets and analysis scripts, enabling collaborators to reproduce analyses with identical parameter settings without requiring detailed written documentation of each parameter value. This addresses reproducibility challenges documented in computational science [@sandve2013ten], where parameter configurations often remain inadequately documented in traditional methods sections. In collaborative projects, shared configuration files ensure consistency across multiple users executing the same analysis pipeline, reducing variability introduced by manual parameter transcription errors. The lightweight nature of YAML configuration files also facilitates inclusion in supplementary materials for scientific publications, providing complete transparency of computational methods.

---

## Research Impact Statement

EZInput addresses the persistent accessibility barrier in computational science by empowering algorithm developers to create user-friendly interfaces with minimal development effort. Through automatic GUI generation, parameter persistence, and cross-environment consistency, the library enables developers to make sophisticated computational methods accessible to end-users, such as experimental biologists, who may lack programming expertise, while simultaneously facilitating systematic testing across diverse computational environments. By requiring only declarative specification of input requirements, EZInput eliminates the substantial interface development overhead whilst maintaining full algorithmic flexibility, allowing developers to focus on their computational methods rather than GUI implementation. The "write once, run anywhere" architecture not only democratizes access for end-users but also streamlines developer workflows, enabling the same parameter configurations to be tested seamlessly from local Jupyter notebooks to cloud platforms to HPC clusters without code modification.

The framework's success is exemplified by its integration into NanoPyx, a high-performance bioimage analysis library, where microscopy researchers leverage EZInput to easily process their images using the methods implemented in NanoPyx \autoref{@fig:nanopyx-example} [@saraiva2025nanopyx]. We have also adapted the ColabFold notebook [@colabfold] to use EZInput for parameter configuration, demonstrating its versatility across diverse scientific domains.

![**Integration of EZInput within NanoPyx enables accessible, reproducible microscopy image analysis.** In NanoPyx, EZInput’s declarative parameter specification automatically produces Jupyter notebook interfaces for complex image processing routines (image registration, denoising, super-resolution reconstruction and image quality assessment). Parameters (numeric ranges, paths, algorithm modes) persist across sessions via lightweight YAML memory, accelerating iterative tuning and ensuring identical settings can be reapplied or shared. This integration lowers the barrier for non-programming users while preserving full algorithmic flexibility, supporting seamless transition from interactive exploration to scripted or HPC execution using the same saved configurations. \label{fig:nanopyx-example}](nanopyx_example.png)

Unlike comprehensive platforms such as CellProfiler [@mcquin2018cellprofiler] or ImageJ/FIJI [@schindelin2012fiji], EZInput functions as a lightweight library integrating into existing Python codebases. Compared to GUI frameworks including ipywidgets, EZInput distinguishes itself through automatic interface generation from declarative specifications, built-in parameter persistence addressing reproducibility, and native terminal support enabling HPC deployment. While web-based frameworks excel at creating dashboards, they require server infrastructure incompatible with many HPC environments where scientific computing occurs. EZInput's minimal dependencies (ipywidgets, prompt_toolkit, PyYAML) facilitate integration without conflicts while enabling developers to validate their tools across multiple execution contexts with identical parameter sets.

Automatic configuration files document exact algorithmic settings, enabling inclusion in supplementary materials, sharing among collaborators for analytical consistency, and version control alongside analysis scripts. Critically, these same configuration files enable systematic testing by allowing developers to define parameter sets once and validate algorithmic behavior across different computational environments. This addresses reproducibility concerns raised by Sandve et al. [@sandve2013ten] regarding inadequate documentation of computational methods as it provides a practical infrastructure for systematic validation workflows.

EZInput's declarative system optimally serves applications with well-defined parameters suitable for standard input types. Applications requiring sophisticated custom visualizations or real-time graphical feedback may benefit from specialized frameworks offering lower-level control, positioning EZInput as complementary to visualization tools like napari [@sofroniew2025napari].

The open-source nature under MIT license facilitates community development, with ongoing priorities including enhanced documentation, cross-environment testing, and integration patterns for common scientific Python frameworks (scikit-learn, scikit-image, PyTorch).
By lowering barriers to creating accessible scientific tools, EZInput enables accessibility considerations to become standard practice rather than optional enhancements. This democratization of interface development parallels the democratization of algorithm access itself, expanding participation in computational science from both developer and user perspectives. As computational methods become increasingly central to scientific inquiry, tools that simultaneously address accessibility and reproducibility through unified architectural design provide valuable contributions to evolving computational research infrastructure.
---

## AI usage disclosure

GitHub copilot with model GPT-4.1 was used for creating automatic documentation and docstrings which were then reviewed and edited by the authors.

LLM model GPT-5 was used as an editorial aid during the preparation of this manuscript to assist with restructuring and clarity. All technical descriptions, claims, and comparisons were written, reviewed, and verified by the authors to ensure correctness and fidelity to the software implementation and existing literature.

---

## Code availability

EZInput is open source and available at  
<https://github.com/HenriquesLab/EZInput>

Demonstrated integrations:
- NanoPyx: <https://github.com/HenriquesLab/NanoPyx>
- ColabFold notebook using EZInput:  
  <https://colab.research.google.com/github/IvanHCenalmor/ColabFold/blob/main/AlphaFold2.ipynb>

---

## Acknowledgements

B.S. and R.H. acknowledge support from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (grant agreement No. 101001332), the Horizon Europe AI4LIFE project (grant agreement 101057970-AI4LIFE), and RT-SuperES (grant agreement 101099654). Additional support was provided by EMBO, the Chan Zuckerberg Initiative, the Research Council of Finland, the Sigrid Juselius Foundation, the Cancer Society of Finland, and the InFLAMES Flagship Programme.
