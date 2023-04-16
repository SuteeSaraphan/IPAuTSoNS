from kubernetes_job import is_active, is_succeeded, is_failed, is_completed, job_status 
from kubernetes_job import JobManager

# get the status of a job
job = manager.read_job(name)

print(f"Status: {job_status(job)}")
print(f"Running: {is_active(job)} Completed: {is_completed(job)}")
print(f"Succeeded: {is_succeeded(job)} Failed: {is_failed(job)}")
