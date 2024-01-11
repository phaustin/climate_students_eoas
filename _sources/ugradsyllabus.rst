Undergraduate Syllabus
=======================================================================================

Climate Modelling: ATSC 448B (directed studies, Jan 2023)
--------------
Python-based introduction to climate modelling and the underlying physics of climate models, 
including a focus on radiation and single-column models as well as atmosphere and ocean
circulation and full general circulation models (GCMs).

Course Purpose
--------------

Students completing this course will be able to describe the different types of climate
models that exist and choose an appropriate model for a given problem. They will be able to
run simple 1D models using jupyter notebooks, and analyse the output from complex General 
Circulation Models (GCMs).

Instructors
-----------

| Rachel White, rwhite@eoas.ubc.ca, Rm 4019 ESB
| Phil Austin, paustin@eoas.ubc.ca

Textbook
-------------
Global Physical Climatology, Dennis Hartmann `available online through the 
UBC library <https://gw2jh3xr2c.search.serialssolutions.com/?sid=sersol&SS_jc=TC0001767901&title=Global%20physical%20climatology>`_

Prerequisites
-------------

One of PHYS 102, PHYS 108, PHYS 118, PHYS 158, PHYS 102, MATH 211, MATH 215, MATH 255, MATH 256, MATH 265.  

Familiarity with python, or strong coding skills in another language (the course is taught in python). 

Familiarity with the basics of global climate science is recommended but not required.   


Course Structure
----------------

This course is not lecture based. The course is an interactive, computer
based laboratory course. The computer will lead you through the
laboratory (like a set of lab notes) and you will answer problems most
of which use the computer. The course consists of three parts: 1) A set of
interactive, computer based laboratory exercises; 2) in-class worksheets, and 3)
a final project.

During the class times, there will be group worksheets to delve
into the material, brief presentations to help with technical
matters and to help you understand some more of the science content, 
time to ask questions in a group format and also individually,
and time to read and work on the laboratories.

It will be important to read the textbook chapters and look through the
labs before class - this will help you to complete the (graded) in-class
worksheets.  To encourage good practices there are quizzes on canvas
for each week.

You can use a web-browser to examine the course exercises. Point your
browser to:

https://phaustin.org/climate_book/home.html

Grades
------

   -  Assignments 50% (individual with collaboration)
   -  Reading Quizzes 5% (individual)
   -  In-class Worksheets 5% (group)
   -  Project Proposal 5%
   -  Project 30% 
   -  Project Oral Presentation 5%

There are 5 worked assignments to complete that are related to the
labs you should have worked through in that week. Assignments can 
be worked with partners or alone, but each student must hand in their 
own solution in their own words.

Reading quizzes are done online, reflect the learning objectives of each week
and are assigned to ensure you do the reading with enough depth to
participate fully in the class worksheets and have the background to
do the Laboratory Exercises.  There will be a "grace space" policy
allowing you to miss one quiz.

The in-class worksheets will be marked for a complete effort. There
will be a “grace space” policy allowing you to miss one class
worksheet. The grace space policy is to accommodate missed classes due
to illness, “away games” for athletes etc. In-class worksheets
are done as a group and are to handed in (one worksheet only per
group) at the end of the worksheet time.

The assignments are to be uploaded to the course CANVAS page. Sometimes, rather than a large series of plots, you may wish to
include a summarizing table. If you do not understand the scope of a
problem, please ask. Help with the labs is
available 1) through piazza (see CANVAS) so you can contact your classmates
and ask them 2) during the weekly scheduled lab or 3) directly from the
instructors. Assignments, quizzes, and the project are expected on
time. Late ones will be marked and then the mark will be multiplied by
:math:`(0.9)^{\rm (number\ of\ days\ or\ part\ days\ late)}`. 


Meeting Times
-------------

?? TBA - this will be decided during the first week of class. 


Tentative schedule, including assignment deadlines
--------

Week 1 (9-15 Jan) Introduction (PA)
   - Introductory Meeting: set class time, introduce jupyter notebooks, github, and the structure of the course

   - Pre-class reading: syllabus

   - Lab: 
      - Notebook 1: Climate models, the global energy budget and Fun with Python


Week 2 (16-22 Jan) - Introduction to Climate Models and the Global Energy Budget (RHW)
   - Pre-class reading: Chapters 1 & 2 of Global Physical Climatology
   
   - Pre-class Quiz #1

   - Labs: 
      - Notebook 2: Modeling the global energy budget
      - Notebook 3: The climate system and climate models

  - Assignment 1 - Climate change in the zero-dimensional EBM - due 9pm Jan 27th - all problems (1 & 2)

Week 3 (23-30 Jan) - Radiative Transfer (PA)
   - Pre-class reading: Chapters 3 & 4 of Global Physical Climatology

   - Pre-class Quiz #2

   - Labs: 
      - Notebook 4: Introducing the Community Earth System Model (CESM)
      - Notebook 5: Building simple climate models using climlab
      - Notebook 6: A Brief Review of Radiation
      - Notebook 7: Elementary greenhouse models

   - Optional lab: Notebook 8

  - Assignment 2 - Global average budgets in the CESM pre-industrial control simulation - due 9pm Feb 3rd - all problems (1 & 2)

Week 4 (30 Jan - 5 Feb) - Radiative Equilibrium and Climate Change (PA)
   - Pre-class reading: Chapter 13 of Global Physical Climatology (and re-cap chapter 3)
   
   - Pre-class Quiz #3

   - Labs: 
      - Notebook 9: Grey radiation modeling with climlab
      - Notebook 10: Modeling non-scattering radiative transfer
      - Notebook 11: Who needs spectral bands? We do. Some baby steps…

   - Assignment 3 - Clouds in the Leaky Greenhouse Model - due 9pm Feb 10th - problems (1, 2, 3, 4, and 5)

Week 5 (6-12 Feb) - Modelling feedbacks and transient warming (PA)
   - Pre-class reading: Chapters 10 of Global Physical Climatology

   - Pre-class Quiz #4

   - Labs: 
      - Notebook 12: Radiative Equilibrium
      - Notebook 13: Radiative-Convective Equilibrium
      - Notebook 14: Climate sensitivity and feedback
      - Notebook 15: Examing the transient and equilibrium CO_2 response in the CESM
      - Notebook 16: Toy models of transient warming

  - Assignment 4 - Feedbacks in the Radiative-Convective Model - due 9pm Feb 17th - all problems (1, 2, 3, 4, and 5)

Week 6 (13-19 Feb) - Modelling climate change (RHW)
   - Pre-class reading: Chapters 11 and 12 of Global Physical Climatology

   - Pre-class Quiz #5

   - Labs: 
      - Notebook 17: Clouds and cloud feedback
      - Notebook 18: Insolation
      - Notebook 19: Orbital variations, insolation, and the ice ages
      - Notebook 20: Heat transport
   
   - Assignment 5 - Climate change in the CESM simulations - due 9pm Mar 3rd - all parts

-- Mid-term break: 20-26 Feb -- 
      

Week 7 (27 Feb - 5 Mar) - Modelling atmospheric general circulation (RHW)
   - Pre-class reading: Chapter 6 of Global Physical Climatology

   - Pre-class Quiz #6

   - Labs: 
      - Notebook 21: The one-dimensional energy balance model
      - Notebook 22: Modeling the seasonal cycle of surface temperature
      - Notebook 23: Atmospheric Dynamics in the CESM
      - Notebook 24: A peek at numerical methods for diffusion models

   - Students choose final project topic from a selection in discussion with instructors

Week 8 (6 - 12 Mar) - Modelling coupled atmosphere-ocean circulation and internal variability (RHW)
   - Pre-class reading: Chapter 7 and 8 of Global Physical Climatology

   - Pre-class Quiz #7

   - Labs: 
      - Notebook 25: Ice-albedo feedback and Snowball Earth in the EBM
      - Notebook 26: Coupled Dynamics in the CESM
      - Notebook: analysis of CESM large ensemble data: https://github.com/NCAR/cesm-lens-aws; 
        running the notebook on `Pangeo <https://aws-uswest2-binder.pangeo.io/v2/gh/NCAR/cesm-lens-aws/binder-config?urlpath=git-pull?repo=https://github.com/NCAR/cesm-lens-aws%26amp%3Bbranch=main%26amp%3Burlpath=lab/tree/cesm-lens-aws/%3Fautodecode>`_ will give you access to the
        large ensemble dataset without having to download it. Login with github (you can create an account for free if you don’t already have one)

   - Project proposal - due 9pm Mar 10th

Week 9 (13 - 19 Mar) - Climate model hierachy and uses (RHW)
   - Pre-class reading: Chapter 9 and re-cap chapters 12 and 13 of Global Physical Climatology (Paleoclimate, Natural Climate Change and Anthropogenic Climate Change)

   - Pre-class Quiz #8

   - Labs: 
      - Notebook 27: The surface energy balance
      - Notebook 28: Land-Ocean contrasts under climate change
      - Notebook 29: Water, water everywhere!

Weeks 10-13 (20 Mar - 13 Apr) - Work on projects
   -  Project Components:
         -  Proposal
         -  10-20 minute presentation to the class
         -  Project report


University Statement on Values and Policies
-------------------------------------------

UBC provides resources to support student learning and to maintain
healthy lifestyles but recognizes that sometimes crises arise and so
there are additional resources to access including those for survivors
of sex- ual violence. UBC values respect for the person and ideas of
all members of the academic community. Harassment and discrimination
are not tolerated nor is suppression of academic freedom. UBC provides
appropriate accommodation for students with disabilities and for
religious and cultural observances. UBC values academic honesty and
students are expected to acknowledge the ideas generated by others and
to uphold the highest academic standards in all of their
actions. Details of the policies and how to access support are
available here

https://senate.ubc.ca/policies-resources-support-student-success.


Supporting Diversity and Inclusion
-----------------------------------

Atmospheric Science, Oceanography and the Earth Sciences have been
historically dominated by a small subset of
privileged people who are predominantly male and white, missing out on
many influential individuals thoughts and
experiences. In this course, we would like to create an environment
that supports a diversity of thoughts, perspectives
and experiences, and honours your identities. To help accomplish this:

  - Please let us know your preferred name and/or set of pronouns.
  - If you feel like your performance in our class is impacted by your experiences outside of class, please don’t hesitate to come and talk with us. We want to be a resource for you and to help you succeed.
  - If an approach in class does not work well for you, please talk to any of the teaching team and we will do our best to make adjustments. Your suggestions are encouraged and appreciated.
  - We are all still learning about diverse perspectives and identities. If something was said in class (by anyone) that made you feel uncomfortable, please talk to us about it


Academic Integrity
------------------

Students are expected to learn material with honesty, integrity, and responsibility.

  - Honesty means you should not take credit for the work of others,
    and if you work with others you are careful to give them the credit they deserve.
  - Integrity means you follow the rules you are given and are respectful towards others
    and their attempts to do so as well.
  - Responsibility means that you if you are unclear about the rules in a specific case
    you should contact the instructor for guidance.

The course will involve a mixture of individual and group work. We try
to be flexible about this as my priority is for you to learn the
material rather than blindly follow rules, but there are
rules. Plagiarism (i.e. copying of others work) and cheating (not
following the rules) can result in penalties ranging from zero on an
assignment to failing the course.



