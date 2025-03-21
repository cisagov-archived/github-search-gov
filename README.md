# github-search-gov #

[![GitHub Build Status](https://github.com/cisagov/github-search-gov/workflows/build/badge.svg)](https://github.com/cisagov/github-search-gov/actions)
[![CodeQL](https://github.com/cisagov/github-search-gov/workflows/CodeQL/badge.svg)](https://github.com/cisagov/github-search-gov/actions/workflows/codeql-analysis.yml)
[![Coverage Status](https://coveralls.io/repos/github/cisagov/github-search-gov/badge.svg?branch=develop)](https://coveralls.io/github/cisagov/github-search-gov?branch=develop)
[![Known Vulnerabilities](https://snyk.io/test/github/cisagov/github-search-gov/develop/badge.svg)](https://snyk.io/test/github/cisagov/github-search-gov)

Scripts to search public GitHub repositories owned by government organizations.

```shell
./setup-env
export GITHUB_TOKEN=$(gh auth token)
export PYTHONUNBUFFERED=true
search-orgs | tee urls.txt
analyze-urls urls.txt | tee results.txt
```

> [!NOTE]
> Expect this to take several minutes to run due to GitHub API rate-limiting.
> You will see back-off messages in the output as the script waits for the
> rate-limit to reset.

## Contributing ##

We welcome contributions!  Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.
