# helix.fhir.client.sdk Upgrade to Version 2.0.8

## Summary

This PR updates the `helix.fhir.client.sdk` package from version 1.0.8 to 2.0.8, along with necessary dependency and Python version updates to maintain compatibility.

## Changes Made

### 1. Package Updates
- **helix.fhir.client.sdk**: 1.0.8 → 2.0.8
- **Python**: 3.7 → 3.12
- **PySpark**: 3.1.x → 3.5.1
- **sparkpipelineframework**: 1.0.26 → 4.0.9
- **sparkautomapper**: 1.0.15 → 3.0.6  
- **sparkfhirschemas**: 1.0.6 → 2.0.4
- **sparkautomapper.fhir**: 1.0.24 → 3.0.3
- **sparkdataframecomparer**: 1.0.4 → 2.0.9
- **sparkpipelineframework.testing**: 1.1.25 → 4.0.5

### 2. Removed Dependencies
- **typed-ast**: Removed (not needed for Python 3.8+, now built-in)

### 3. Configuration Files Updated
- `Pipfile`: Updated all package versions and Python version
- `setup.py`: Updated python_requires to >=3.12
- `.github/workflows/bulild_and_test.yml`: Updated Python version to 3.12
- `.github/workflows/python-publish.yml`: Updated Python version to 3.12
- `pre-commit.Dockerfile`: Updated base image to python:3.12-slim
- `spark.Dockerfile`: Updated base image to imranq2/helix.spark:3.5.1.9-slim

## Why These Changes?

1. **helix.fhir.client.sdk 2.0.8 requires Python 3.10+**: Version 2.x of the SDK dropped support for Python 3.7-3.9 and requires Python 3.10 or higher.

2. **PySpark 3.1 doesn't support Python 3.10+**: The old PySpark version (3.1.x) only supports Python 3.6-3.9, so we needed to upgrade to PySpark 3.5.1 which supports Python 3.10-3.12.

3. **Spark-related packages needed updates**: All Spark ecosystem packages (sparkpipelineframework, sparkautomapper, etc.) needed to be updated to versions compatible with PySpark 3.5.x.

4. **Python 3.12 chosen**: While 3.10+ would work, we chose 3.12 as it's the latest stable version and provides better performance and features.

## helix.fhir.client.sdk 2.0.8 Changes

Key differences between v1.0.8 and v2.0.8:
- **Python 3.10+ requirement**: Dropped support for older Python versions
- **Enhanced logging**: Improved logging capabilities
- **Simulated $graph support**: Added support for simulating $graph calls when servers don't support them
- **Additional features**: Version 2.x adds several new features for FHIR resource handling

## Code Impact

**No code changes required**: The `helix.fhir.client.sdk` package is declared as a dependency but is not currently imported or used anywhere in the codebase. Therefore, no code updates are needed to accommodate API changes.

## Next Steps

### Pipfile.lock Generation

The `Pipfile.lock` file needs to be regenerated with the new dependencies. This will happen automatically when the CI/CD pipeline builds the project using Docker:

```bash
# This will run automatically in CI/CD
docker-compose run --rm dev pipenv lock --dev
```

The Docker build environment handles SSL certificates properly and will generate the lock file during the PR build process.

### Testing

Once the lock file is generated:
1. The CI/CD pipeline will run all existing tests
2. Verify the build completes successfully
3. Check that there are no dependency conflicts

## Rollback Plan

If issues arise, the changes can be rolled back by:
1. Reverting this commit
2. The old Pipfile.lock will be restored automatically
3. No code changes needed as the SDK isn't actively used

## References

- [helix.fhir.client.sdk GitHub](https://github.com/icanbwell/helix.fhir.client.sdk)
- [helix.fhir.client.sdk Documentation](https://icanbwell.github.io/helix.fhir.client.sdk/)
- [PySpark Version Support Matrix](https://spark.apache.org/docs/latest/)
