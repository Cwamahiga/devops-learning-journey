# Week 1 – Day 2 : COMPUTE IN THE CLOUD & AUTOSCALING/LOAD BALANCING

**Date:** 17/11/2025  
**Duration:** ~1 hour  

---

## 📚 What I Learned Today

### 1️⃣ Compute in the Cloud

#### **Amazon EC2 Overview**
- EC2 (Elastic Compute Cloud) = virtual servers in the cloud.
- Allows **on-demand compute** without managing physical servers.
- Provides **full control** over:
  - Operating System (Linux, Windows)
  - Storage (EBS volumes, instance store)
  - Networking (VPC, subnets, security groups)
- Benefits: scalability, flexibility, cost-efficient for variable workloads.

#### **EC2 Instance Types**
- Choose based on workload to optimize **cost vs performance**.
- **General Purpose:** balanced CPU, memory, networking; ideal for web servers, dev/test environments. Example: `t2.micro` (1 vCPU, 1GB RAM, Free Tier).  
- **Compute Optimized:** high CPU; good for batch processing, HPC, gaming servers. Example: `c5.large` (2 vCPU, 4GB RAM).  
- **Memory Optimized:** high RAM; ideal for in-memory databases, caching. Example: `r5.large` (2 vCPU, 16GB RAM).  
- **Storage Optimized:** high IOPS ((Input/Output Operations Per Second)); good for NoSQL, warehousing, logging. Example: `i3.large` (2 vCPU, 15.25GB RAM, NVMe SSD).

#### **Amazon Machine Images (AMI)**
- AMI = blueprint/template for launching EC2 instances.
- Contains:
  - Operating System
  - Storage configuration
  - Architecture type (x86/ARM)
  - Launch permissions
  - Pre-installed software
- Benefits:
  - Repeatable deployments
  - Consistent dev/test/prod environments
- **Three ways to use AMIs:**
  1. **Custom AMI:** tailored to your applications and configuration.
  2. **AWS-provided AMIs:** pre-configured OS templates.
  3. **Marketplace AMIs:** third-party software (licensed or specialized).

#### **Provisioning EC2**
- Methods:
  - AWS Management Console (GUI)
  - AWS CLI (automation/scripts)
  - AWS SDKs (integrate into applications)
- **Shared Responsibility Model:**
  - AWS → Security **of** the cloud (hardware, network, hypervisor)
  - Customer → Security **in** the cloud (OS, apps, data, IAM)
- **Managed vs Unmanaged Services**
  - **Unmanaged:** customer configures everything (EC2, self-managed OS, patches)
  - **Managed:** AWS handles infrastructure/OS (RDS, S3, Lambda)

#### **Launching an EC2 Instance (Hands-On)**
- Steps:
  1. Choose instance **name**
  2. Select **AMI** (e.g., Amazon Linux)
  3. Pick **instance type** (e.g., `t2.micro`)
  4. Configure **key pair** (public/private key)
  5. Configure **network/security groups** (allow HTTP for web server)
  6. Configure **storage** (EBS gp3 volume, e.g., 8GB)
  7. Add **User Data script** (to auto-install Nginx web server)
  8. Launch instance
- Verify by accessing **public IP** in a browser

#### **EC2 Pricing**
- **On-Demand:** pay per second/hour; no commitment.  
- **Savings Plans:** commit 1–3 years; up to 72% savings.  
- **Reserved Instances (RI):** steady workloads; up to 75% discount; payment: all upfront, partial, none.  
- **Spot Instances:** spare capacity; up to 90% discount; can be interrupted.  
- **Dedicated Hosts:** full physical server; good for compliance or license-bound workloads.  
- **Capacity Reservations:** reserve compute in a specific AZ; pay On-Demand rate even if unused.

#### **Messaging & Queuing**
- Decouple applications for reliability/resilience.
- **Tightly coupled:** direct calls; failure cascades.
- **Loosely coupled:** use buffers/queues; failure isolated.
- AWS services:
  - **SQS:** reliable message queue; stores messages until processed; auto-scalable.  
  - **SNS:** publish-subscribe; immediate delivery; supports fan-out to SMS, email, push.  
  - **EventBridge:** serverless event bus; route events between applications and services.

---

### 2️⃣ Auto Scaling & Load Balancing

#### **Scalability vs Elasticity**
- **Scalability:** system’s ability to grow capacity over time.  
- **Elasticity:** dynamic adjustment of resources based on demand.

#### **EC2 Auto Scaling**
- Automatically adjusts instances based on traffic/workload.
- Uses **CloudWatch metrics** (CPU, latency, performance) to trigger scaling.
- **Dynamic scaling:** real-time adjustments.  
- **Predictive scaling:** pre-schedules resources based on expected demand.
- **Auto Scaling Groups:** define minimum, maximum, and desired instance counts.

#### **Elastic Load Balancing (ELB)**
- Distributes incoming traffic across multiple EC2 instances.
- Single entry point for Auto Scaling Groups.
- Works with Auto Scaling to ensure **high availability** and **consistent performance**.
- **Routing methods:**
  - Round Robin – evenly distribute requests
  - Least Connections – server with fewest active connections
  - IP Hash – consistently route client to same server
  - Least Response Time – server with fastest response

---

## 💡 Key Takeaways
1. EC2 provides flexible compute options with various pricing and scaling choices.  
2. Choosing the right **instance type** is critical for performance and cost.  
3. AMIs enable repeatable, consistent deployments.  
4. Auto Scaling + ELB ensures high availability and performance under changing workloads.  
5. Loosely coupled architectures (SQS/SNS) improve reliability and resilience.

---

## 🚧 Challenges Faced
- Confusion between **Dedicated Hosts vs Dedicated Instances**  
- Selecting the correct **EC2 instance type** for specific workloads  

---

## 💻 Hands-On Practice
- Launched EC2 instance with Amazon Linux.  
- Configured **Nginx** using User Data script.  
- Created **Auto Scaling Group** and tested dynamic scaling.  
- Configured **ELB** and tested traffic routing.  
- Practiced **SQS** and **SNS** messaging scenarios.

---

## 🎯 Tomorrow’s Plan
- Explore EC2 **instance families** in more detail.  
- Dive deeper into **Auto Scaling policies**.  
- Learn advanced **messaging patterns** in AWS.
