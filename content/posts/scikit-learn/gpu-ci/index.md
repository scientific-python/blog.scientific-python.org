---
title: "Automated tests with GPUs for your project"
date: 2024-08-15
draft: false
description: "Setting up CI with a GPU to test your code"
tags: ["scikit-learn", "ci", "gpu", "cuda"]
displayInList: true
author: ["Tim Head <timhead>"]
canonicalURL: https://betatim.github.io/posts/github-action-with-gpu/
---

TL;DR: If you have GPU code in your project, setup a GitHub hosted GPU runner today.
It is fairly quick to do and will free you from having to run tests manually.

Writing automated tests for your code base and certainly for the more complex parts
of it has become as normal as brushing your teeth in the morning. Having a system
that automatically runs a project's tests for every Pull Request
is completely normal. However, until recently it was very complex and expensive
to setup a system that can run tests on a system with a GPU. This means that,
when dealing with GPU related code, we were thrown back into the dark ages where
you had to rely on manual testing.

In this blog post I will describe how we set up a GitHub Action based GPU runner
for the scikit-learn project and the things we learnt along the way. The goal is
to give you some additional information and details about the setup we now use.

- [Setting up larger runners for your project](#larger-runners-with-gpus)
- [VM image contents and setup](#vm-image-contents)
- [Workflow configuration](#workflow-configuration)
- [Bonus material](#bonus-material)

## Larger runners with GPUs

All workflows for your GitHub project are executed on a
runner. Normally all your workflows run on the default runner, but you can have additional runners too. If you wanted
to you could host a runner yourself on your own infrastructure. Until now this
was the only way to get access to a runner with a GPU. However, hosting your
own runner is complicated and comes with pitfalls regarding security.

Since about April 2024 GitHub has made [larger runners with a
GPU](https://docs.github.com/en/actions/using-github-hosted-runners/about-larger-runners/about-larger-runners) generally available.

To use these you will have to [setup a credit card for your organisation](https://docs.github.com/en/billing/managing-your-github-billing-settings/adding-or-editing-a-payment-method#updating-your-organizations-payment-method). Configure a spending limit so that you do not end up getting surprised
with a very large bill. For scikit-learn we currently use a limit of $50.

When [adding a new GitHub hosted runner](https://github.com/organizations/YOUR_OWN_ORG_NAME/settings/actions/runners) make sure to select the "Partner" tab when
choosing the VM's image. You need to select the "NVIDIA GPU-Optimized Image for AI and HPC"
image in order to be able to choose the GPU runner later on.

The group the runner is assigned to can be configured to only allow particular repositories
and workflows to use the runner group. It makes sense to only enable the runner
group for the repository in which you plan to use it. Limiting which workflows your
runner will pick up requires an additional level of indirection in your workflow
setup, so I will not cover it in this blog post.

Name your runner group `cuda-gpu-runner-group` to match the name used in the examples
below.

## VM Image contents

The GPU runner uses a disk image provided by NVIDIA. This means that there are
some differences to the image that the default runner uses.

The `gh` command-line utility is not installed by default. Keep this in mind
if you want to do things like removing a label from the Pull Request or
other such tasks.

The biggest difference to the standard image is that the GPU image contains
a conda installation, but the file permissions do not allow the workflow user
to modify the existing environment or create new environments. As a result
for scikit-learn we install conda a second time via miniforge. The conda environment is
created from a lockfile, so we do not need to run the dependency solver.

## Workflow configuration

A key difference between the GPU runner and the default runner is that a project
has to pay for the time of the GPU runner. This means that you might want to
execute your GPU workflow only for some Pull Requests instead of all of them.

The GPU available in the runner is not very powerful, this means it is not
that attractive of a target for people who are looking to abuse free GPU resources.
Nevertheless, once in a while someone might try. Another reason to not run
the GPU workflow by default.

A nice way to deal with running the workflow only after some form of human review
is to use a label. To mark a Pull Request (PR) for execution on the GPU runner a
reviewer applies a particular label. Applying a label does not cause a notification
to be sent to all PR participants, unlike using a special comment to trigger the
workflow.
In the following example the `CUDA CI` label is used to mark a PR for execution and
the `runs-on` directive is used to select the GPU runner. This is a snippet from
[the full GPU workflow](https://github.com/scikit-learn/scikit-learn/blob/9d39f57399d6f1f7d8e8d4351dbc3e9244b98d28/.github/workflows/cuda-ci.yml) used in the scikit-learn repository.

```
name: CUDA GPU
on:
  pull_request:
    types:
      - labeled

jobs:
  tests:
    if: contains(github.event.pull_request.labels.*.name, 'CUDA CI')
    runs-on:
      group: cuda-gpu-runner-group
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12.3'
      - name: Checkout main repository
        uses: actions/checkout@v4
      ...
```

In order to remove the label again we need a workflow with elevated
permissions. It needs to be able to edit a Pull Request. This privilege is not
available for workflows triggered from Pull Requests from forks. Instead
the workflow has to run in the context of the main repository and should only
do the minimum amount of work.

```
on:
  # Using `pull_request_target` gives us the possibility to get a API token
  # with write permissions
  pull_request_target:
    types:
      - labeled

# In order to remove the "CUDA CI" label we need to have write permissions for PRs
permissions:
  pull-requests: write

jobs:
  label-remover:
    if: contains(github.event.pull_request.labels.*.name, 'CUDA CI')
    runs-on: ubuntu-20.04
    steps:
      - uses: actions-ecosystem/action-remove-labels@v1
        with:
          labels: CUDA CI
```

This snippet is from the [label remover workflow](https://github.com/scikit-learn/scikit-learn/blob/9d39f57399d6f1f7d8e8d4351dbc3e9244b98d28/.github/workflows/cuda-label-remover.yml)
we use in scikit-learn.

## Bonus Material

For scikit-learn we have been using the GPU runner for about six weeks. So far we have stayed
below the $50 monthly spending limit we set. This includes some runs to debug the setup at the
start.

One of the scikit-learn contributors created a [Colab notebook that people can use to setup and run the scikit-learn test suite on Colab](https://gist.github.com/EdAbati/ff3bdc06bafeb92452b3740686cc8d7c). This is useful
for contributors who do not have easy access to a GPU. They can test their changes or debug
failures without having to wait for a maintainer to label the Pull Request. We plan to add
a workflow that comments on PRs with information on how to use this notebook to increase its
discoverability.

## Conclusion

Overall it was not too difficult to setup the GPU runner. It took a little bit of fiddling to
deal with the differences in VM image content as well as a few iterations for how to setup
the workflow, given we wanted to manually trigger them.

The GPU runner has been reliably working and picking up work when requested. It saves us (the
maintainers) a lot of time, as we do not have to checkout a PR locally and run the tests
by hand.

The costs so far have been manageable and it has been worth spending the money as it removes
a repetitive and tedious manual task from the reviewing workflow. However, it does require
having the funds and a credit card.
