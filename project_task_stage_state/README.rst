=================================
Add State field to Project Stages
=================================

.. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fproject-lightgray.png?logo=github
    :target: https://github.com/OCA/project/tree/15.0/project_task_stage_state
    :alt: OCA/project
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/project-15-0/project-15-0-project_task_stage_state
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runbot-Try%20me-875A7B.png
    :target: https://runbot.odoo-community.org/runbot/140/15.0
    :alt: Try me on Runbot

|badge1| |badge2| |badge3| |badge4| |badge5| 

This module restores the `state` fields to Project Stages, removed in Odoo 8.0.

For some use cases it‘s necessary to be able to map the multiple Stages into
a few broad groups.

For example, this can allow to define automated actions and business logic for
Tasks not yet “Started”, knowing that “Started” means different Stages in
different Projects.

**Table of contents**

.. contents::
   :local:

Configuration
=============

You can configure stages from Project -> Configuration -> Stages

Usage
=====

To use this module, you need to:

#. Go to Project -> Configuration -> Stages and click on a stage
#. Select the state you would like to associate that stage with from the dropdown "State" menu
#. Save your changes
#. Go to Project -> Dashboard and click on the Task button for a specific project.
#. Click on task and it's specific stage, the state field associated with it will change accordingly.
#. Under the "Customer" field, you can see the "State" field for that task.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/project/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/OCA/project/issues/new?body=module:%20project_task_stage_state%0Aversion:%2015.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Daniel Reis

Contributors
~~~~~~~~~~~~

- Daniel Reis
- Rodrigo Ferreira <rodrigosferreira91@gmail.com>
- Anand Kansagra <kansagraanand@hotmail.com>
- Saran Lim. <saranl@ecosoft.co.th>
- Nattapol Sinsuphan<gamso321@gmail.com>
- Manuel Regidor <manuel.regidor@sygel.es>

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/project <https://github.com/OCA/project/tree/15.0/project_task_stage_state>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
