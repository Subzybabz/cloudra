
## **DESIGN AND IMPLEMENTATION OF A CLOUD MIGRATION RISK** 

**ASSESSMENT DATABASE SYSTEM USING AMAZON DYNAMODB** 

**BY** 

## **OGUNBANJO OLASUBOMI JESULOBA** 

**23/12987** 

**A PROJECT SUBMITTED TO THE DEPARTMENT OF COMPUTER SCIENCE,** 

**COLLEGE OF COMPUTING AND INFORMATION SCIENCES** 

**IN PARTIAL FULFILLMENT OF THE REQUIREMENT OF THE AWARD OF BACHELOR OF SCIENCE (B.Sc) DEGREE IN COMPUTER SCIENCE.** 

**JUNE 2026.** 


## **Chapter 1** 

## **INTRODUCTION** 

## **1.0 Background of the Study** 

The modern enterprise is undergoing a profound technological transformation; one that is reshaping how organisations acquire, deploy, and manage their information technology (IT) infrastructure. At the centre of this transformation is cloud computing- a paradigm that has fundamentally altered the traditional model of owning and operating on-premise data centres, replacing it with a flexible, scalable, and consumption-based model of accessing computing resources over the internet. This transition from traditional, on-premise (commonly referred to as "on-prem") data centre environments to cloud computing platforms represents one of the most consequential strategic decisions that modern organisations face. It is a decision that touches every dimension of organisational operations from the technical configuration of servers and storage systems, to financial planning and budgeting cycles, to the governance of sensitive corporate and customer data. 

Historically, organisations have managed their IT needs by investing in physical infrastructure housed within their own facilities or dedicated co-location data centres. This model is characterised by large upfront capital investments in hardware, software licences, and skilled personnel, providing organisations with complete control over their computing environments. However, it also imposed significant limitations such as scaling capacity required lengthy procurement cycles and substantial capital expenditure, maintaining hardware demanded specialist expertise and continuous operational overhead, and geographic redundancy or disaster recovery required the duplication of entire infrastructure stacks at secondary sites. These limitations became increasingly problematic as the pace of digital commerce accelerated and the demand for agile, globally accessible systems 


intensified. 

Cloud computing emerged as the answer to these limitations. Pioneered by providers such as Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP), cloud computing delivers on-demand access to a shared pool of configurable computing resources including servers, storage, databases, networking, analytics, and artificial intelligence over the internet, with costs tied to actual consumption rather than fixed capital investment. The National Institute of Standards and Technology (NIST) formally defines cloud computing as "a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources that can be rapidly provisioned and released with minimal management effort or service provider interaction" (Mell & Grance, 2011). This definition captures the essential promise of cloud computing: flexibility, speed, and efficiency without the burden of infrastructure management. 

The commercial adoption of cloud computing has grown at a remarkable pace. According to the Flexera State of the Cloud Report (2023), over 92% of enterprises now operate in multicloud environments with global cloud infrastructure spending exceeding $200 billion in 2022. Organisations across all sectors from the finance and healthcare to education, manufacturing, and the public sectors are actively migrating their workloads from on-premise systems to cloud environments. The drivers of this migration are well-documented; cloud platforms offer elastic scalability that allow organisations to rapidly expand or contract their computational capacity in response to demand. They also provide geographic redundancy and high-availability architectures that would be prohibitively expensive to replicate onpremise. They enable organisations to access cutting-edge technologies such as machine learning, big data analytics, and serverless computing without building bespoke infrastructure. They also offer a consumption-based financial model that converts large, irregular capital expenditures into predictable, manageable operational costs. 


Despite the compelling strategic advantages of cloud adoption, the process of migrating existing IT infrastructure from on-premise environments to the cloud is far from straightforward. Cloud migration is a deeply complex, multidimensional undertaking that involves not merely the technical act of moving data and applications from one location to another, but a comprehensive re-engineering of how an organisation's IT systems are architected, secured, managed, and funded. Each migration project is unique, shaped by the organisation's specific combination of legacy systems, application dependencies, data sensitivity requirements, compliance obligations, financial constraints, and technical expertise. The complexity of this process is compounded by the fundamental differences between on-premise and cloud computing environments- the cloud operates on a shared, virtualised infrastructure governed by a Shared Responsibility Model where security and compliance obligations are distributed between the cloud provider and the customer in ways that are often poorly understood by organisations making the transition. 

The risks associated with cloud migration are well-documented and span three principal dimensions. Operationally, migration projects are vulnerable to system downtime, data corruption or loss during transfer, network reconfiguration errors, and the disruption of application services due to unmapped dependencies between systems. The financial dimension of migration risk is equally significant; the transition from a Capital Expenditure (CapEx) model where IT costs are fixed, predictable, and depreciated over time to an Operational Expenditure (OpEx) model where costs fluctuate based on dynamic, usage-based cloud billing introduces significant financial forecasting complexity. Organisations that do not rigorously model their projected cloud consumption frequently experience what the industry has termed "cloud bill shock"- the receipt of unexpectedly high cloud invoices driven by over-provisioned resources, unanticipated data egress fees, and the cumulative cost of services inadvertently left running. The Flexera (2023) report found that organisations waste 


an average of 32% of their total cloud spend, a direct consequence of inadequate premigration financial planning. 

The cybersecurity dimension of cloud migration risk is perhaps the most consequential. Moving data and applications to the cloud fundamentally changes the security perimeter; the traditional model of protecting an organisation's assets within a clearly defined network boundary is replaced by a cloud-native security model in which data may be distributed across multiple regions and accessed from any device or location. Misconfigurations, particularly overly permissive Identity and Access Management (IAM) policies and publicly exposed cloud storage buckets have consistently been identified as the leading cause of cloud data breaches. The 2023 Verizon Data Breach Investigations Report found that misconfiguration was a contributing factor in over 21% of cloud-related security incidents, affirming the critical importance of proactive security assessment prior to migration. 

Recognising and quantifying these multidimensional risks: **Operational, Financial, and Cybersecurity** , is therefore essential for any organisation seeking to undertake cloud migration responsibly. Effective risk assessment requires not only a deep understanding of the technical and commercial dynamics of cloud computing, but also a structured, systematic methodology for evaluating the specific characteristics of a proposed migration against established risk thresholds. Yet despite the high stakes involved, the tools and methodologies available to project managers and IT auditors for this purpose remain surprisingly limited. Most organisations continue to rely on manual, spreadsheet-based risk registers and static assessment frameworks that are fundamentally ill-equipped to capture the dynamic, and realtime nature of cloud environments. 

This study is motivated by the recognition that there exists a critical procedural gap in the field of IT project management and cloud governance: the absence of an automated, datadriven, web-based tool capable of dynamically assessing cloud migration risk across 


operational, financial, and cybersecurity dimensions simultaneously, and translating that assessment into a quantified, actionable risk score supported by specific mitigation recommendations. This project addresses that gap by designing, developing, and deploying precisely such a system- a serverless, API-driven risk assessment web application built on Amazon Web Services, capable of evaluating migration parameters in real time against live cloud pricing data and established security benchmarks, and generating compliance-grade audit reports suitable for distribution to project stakeholders and executive leadership. 

## **1.1 Statement of the Problem** 

Despite the scale and complexity of cloud migration as an enterprise undertaking, there is a notable and persistent absence of automated, data-driven tools capable of dynamically evaluating the full spectrum of risks associated with migrating on-premise IT infrastructure to cloud environments. The tools and processes that currently exist for this purpose suffer from fundamental limitations that leave organisations systematically exposed to operational disruption, financial overruns, and security breaches. 

The predominant approach to cloud migration risk assessment in current practice is the static risk register- a document that is typically maintained in spreadsheet form, that catalogues identified risks, assigns subjective likelihood and impact ratings, and records planned mitigation actions. While universally adopted in project management practice, static risk registers are structurally unsuited to the demands of cloud migration assessment. They are point-in-time documents that capture the state of identified risks at the moment of their creation but are rarely updated with sufficient frequency to remain relevant throughout the duration of a migration project. They rely on qualitative, subjective ratings typically expressed as **High, Medium, or Low** that lack the quantitative rigour necessary for financial forecasting or executive decision-making. Most critically, they cannot integrate with live data sources, they cannot query real-time cloud pricing APIs to reflect current cost models, nor 


can they evaluate the specific configuration of a proposed cloud environment against current security compliance benchmarks. The result is a significant and dangerous gap between the static picture presented in the risk register and the dynamic reality of the cloud environment being deployed. 

From a security perspective, the paradigm shift from traditional, perimeter-based network security to cloud-native security architectures presents a steep learning curve for organisations making the migration. The Shared Responsibility Model- which defines how security obligations are divided between the cloud service provider and the customer is widely misunderstood. Many organisations migrating from on-premise environments incorrectly assume that the cloud provider bears responsibility for securing the data and applications that the customer deploys on its infrastructure, when in fact the customer retains full responsibility for data classification, identity management, operating system configurations, and network controls within their cloud tenancy. This misunderstanding manifests in catastrophic misconfigurations; overly permissive IAM roles that grant excessive access to cloud resources, publicly exposed storage buckets containing sensitive data, and inadequate encryption of data in transit and at rest. Traditional, static risk registers cannot capture the granular, constantly changing configurations of cloud environments and therefore consistently fail to identify these critical vulnerabilities before they result in data breaches. 

The financial dimension of the problem is equally acute. The transition from a Capital Expenditure (CapEx) model to an Operational Expenditure (OpEx) model fundamentally changes how IT costs are incurred and accounted for. On-premise hardware costs are fixed, predictable, and depreciated over multi-year cycles, making them relatively straightforward to budget. Cloud costs, by contrast, are variable and consumption-based- accruing on a persecond, per-request, or per-gigabyte basis and can fluctuate dramatically based on usage 


patterns, data transfer volumes, and the configuration of cloud services. Traditional IT budgeting tools, which are designed around fixed-cost assumptions, are fundamentally inadequate for modelling the elastic, usage-based billing of cloud environments. Manual calculators and spreadsheet models cannot accurately simulate the complex interaction of computational costs, storage costs, data egress fees, and the potential for runaway spending caused by auto-scaling resources that exceed their intended limits. This inadequacy directly contributes to the widespread phenomenon of cloud bill shock, where misprovisioned resources and unanticipated fees cause recurring cloud costs to severely outpace initial projections. 

Operationally, cloud migration projects require a sophisticated analysis of data gravity (the tendency of large datasets to attract associated processing and applications), application dependencies, and network latency constraints that existing manual assessment frameworks are poorly equipped to conduct. By relying on intuition and static questionnaires rather than programmatic evaluation of specific infrastructure characteristics, IT teams risk deploying migration plans that result in severe performance bottlenecks, extended system downtime during the cutover phase, and the discovery of previously unidentified interdependencies between legacy applications that prevent successful migration without extensive reengineering. 

Ultimately, the absence of an integrated, API-driven risk assessment engine that can dynamically evaluate these operational, financial, and cybersecurity dimensions simultaneously and translate the results into a unified, quantified risk score with actionable mitigation guidance represents a critical void in current IT project management practice. Without such a system, organisations undertaking cloud migration remain fundamentally exposed to the risk of systemic project failure, with consequences that may include reputational damage from publicised data breaches, regulatory sanctions for compliance 


violations, and financial losses from service disruptions and cost overruns. This study is designed to address this void directly. 

## **1.2 Aims and Objectives of the Study** 

## _**1.2.1 Aim**_ 

The primary aim of this study is to design, develop, and implement a web-based, automated risk assessment system that provides quantified risk scores and actionable mitigation strategies for enterprise cloud migration projects, thereby replacing static, manual risk assessment approaches with a dynamic, data-driven tool capable of evaluating operational, financial, and cybersecurity risks in real time. 

## _**1.2.2 Specific Objectives**_ 

To achieve the primary aim, the study pursues the following specific objectives: 

1. To conduct a comprehensive review of existing literature on cloud computing, cloud migration strategies, IT risk management frameworks, cloud security governance, and financial risk modeling in order to establish the theoretical and empirical foundations for the system's design. 

2. To design and develop a highly responsive, intuitive frontend dashboard using HTML5, CSS3, and Vanilla JavaScript that enables project managers and IT auditors to input migration parameters and visualise real-time risk analytics through interactive charts and gauges. 

3. To engineer a serverless backend infrastructure on Amazon Web Services (AWS), utilising AWS API Gateway and Python-based AWS Lambda functions, to process risk assessment requests with high availability, automatic scalability, and minimal operational overhead. 


4. To implement a proprietary, three-dimensional risk scoring algorithm that evaluates submitted migration parameters across operational, financial, and cybersecurity risk dimensions, incorporating live AWS pricing data retrieved via the Boto3 SDK to ensure that financial risk scores reflect current market rates. 

5. To design a data persistence layer using Amazon DynamoDB that maintains an immutable audit trail of all generated risk assessments, supporting compliance reporting and forensic review requirements. 

6. To develop an automated PDF compliance report generation module that compiles computed risk scores, identified vulnerabilities, and recommended mitigation strategies into professionally formatted reports suitable for distribution to project stakeholders, executive leadership, and compliance auditors. 

7. To validate the correctness, performance, security, and usability of the developed system through a multi-level testing strategy comprising unit testing, integration testing, system testing, user acceptance testing, and performance benchmarking. 

## **1.3 Rationale and Justification of the Study** 

The rationale for this study is grounded in the convergence of three critical realities: the rapid and accelerating pace of enterprise cloud adoption, the demonstrated inadequacy of existing risk assessment tools and methodologies for cloud migration contexts, and the significant and well-documented consequences of cloud migration failures for organisations that proceed without adequate risk quantification. 

Cloud migration has transitioned from a technology experiment to a strategic imperative for organisations across all sectors. The global cloud computing market is projected to exceed $1 trillion by 2026 (Gartner, 2022), and the pressure on IT leaders to migrate workloads to the cloud driven by the competitive advantages of scalability, agility, and access to advanced 


cloud-native services is intense and growing. Yet, the complexity of cloud migration has not diminished with the maturation of cloud platforms; if anything, the increasing sophistication of cloud architectures, the proliferation of cloud services, and the evolving landscape of cloud security threats have made the risk management challenge more demanding, not less. 

The consequences of inadequate risk assessment prior to cloud migration are severe and wellevidenced. The IDC (2019) estimated that unplanned downtime during cloud migration costs enterprises an average of **$250,000 per hour** , and the Ponemon Institute (2022) reported the average cost of a data breach- many of which originate from cloud misconfigurations at **$4.35 million** . Beyond the direct financial costs, organisations that experience significant migration failures face reputational damage, loss of customer trust, regulatory sanctions, and the substantial cost of remediation. These consequences are not theoretical risks but documented outcomes of real migration projects that proceeded without adequate risk quantification. 

The existing landscape of cloud migration risk assessment tools is demonstrably insufficient to address these challenges. Commercial tools such as AWS Migration Evaluator, Cloudamize, and Azure Migrate focus primarily on infrastructure discovery and financial modeling for a single cloud provider, and do not offer integrated cybersecurity risk assessment or a unified composite risk score. Academic frameworks for cloud migration risk assessment, while theoretically sound, have not been translated into deployable, real-world tools that project managers can access and use. The gap between theoretical frameworks and practical tools is therefore wide and this gap is exactly what the proposed system is designed to bridge. 

The justification for a serverless, API-driven approach to this problem is also well-founded. The use of AWS Lambda and API Gateway for the backend compute layer means that the system can scale automatically to accommodate concurrent assessment requests without 


requiring the provisioning or management of server infrastructure- a design choice that eliminates a class of operational risk and reduces the total cost of system ownership. The integration of live AWS pricing data via the Boto3 SDK addresses a specific and critical gap identified in the literature; the inability of existing tools and academic models to provide financial risk scores that reflect current, real-time cloud pricing rather than static pricing tables that rapidly become outdated. 

Furthermore, the use of Amazon DynamoDB for immutable audit trail persistence addresses the compliance documentation requirements of regulated industries- a feature that is conspicuously absent from existing migration assessment tools. 

In summary, this study is justified by the scale of the problem it addresses, the inadequacy of existing solutions, and the feasibility and appropriateness of the technical approach adopted. The proposed system represents a novel, practical, and academically grounded contribution to the field of IT project risk management that fills a demonstrated gap in both the academic literature and the commercial tooling landscape. 

## **1.4 Significance of the Study** 

This study makes significant contributions at multiple levels- **practical, organizational, academic, and professional** - by bridging a critical gap between the static, manual risk assessment methods currently employed in cloud migration projects and the dynamic, datadriven capabilities that modern cloud environments demand. 

**For Project Managers** , the system transforms the risk assessment process from a reactive, subjective exercise into a predictable, data-backed discipline. Rather than relying on expert judgment and experience to estimate the risks associated with a proposed migration, project managers can submit specific, quantifiable migration parameters and receive a computed risk score calibrated against empirically established thresholds. **The interactive dashboard** 


**categorises risks as High, Medium, or Low across Operational, Financial, And Cybersecurity dimensions** , enabling project managers to identify the dominant sources of vulnerability in their migration plans and allocate resources, adjust timelines, and apply targeted mitigation strategies before the migration cutover begins- a shift from reactive crisis management to proactive risk governance. 

**For IT Auditors and Security Teams** , the system enforces a shift-left security philosophy by enabling architectural plans to be evaluated against security benchmarks before they are deployed to production environments. The immutable DynamoDB audit trail and automated PDF compliance reports ensure that there is a documented, verifiable record of every risk assessment conducted, demonstrating to regulators and auditors that due diligence was exercised in identifying and addressing security vulnerabilities. This capability is particularly valuable for organisations operating under regulatory frameworks such as GDPR, HIPAA, or PCI DSS, which impose explicit documentation requirements for risk management processes. 

**For Organisations** , the system functions as a financial safeguard against cloud bill shockthe widespread phenomenon of receiving unexpectedly high cloud invoices post-migration. By incorporating real-time AWS pricing data into the financial risk sub-score calculation, the system provides organisations with a financially grounded assessment of their projected cloud costs before any resources are provisioned. This proactive financial modeling prevents the over-provisioning of cloud resources and enables organisations to make informed decisions about their migration strategy with a clear understanding of the financial risks involved. 

**For Executive Leadership** , including Chief Information Officers (CIOs), Chief Technology Officers (CTOs), and Chief Financial Officers (CFOs), the system translates complex, multidimensional technical vulnerabilities into clear, quantified business risks expressed on a simple 0-to-100 scale. This level of transparency empowers C-suite decision-makers to evaluate the true Return on Investment (ROI) of a proposed cloud migration, assess whether 


the identified risk profile falls within the organisation's established risk appetite, and make strategically informed decisions about the timing, scope, and approach of their migration projects. 

**For the Academic and Professional Community** , this study contributes a practical, documented implementation of a serverless, API-driven risk assessment system that demonstrates how cloud-native architectures can be applied to solve real-world problems in IT project risk management. The detailed documentation of the system's architecture, algorithm design, and testing methodology provides a reproducible blueprint that researchers and practitioners can build upon, extend, and adapt for related risk assessment challenges in cloud governance, compliance automation, and FinOps practice. 

## **1.5 Scope of the Study** 

This study focuses exclusively on the design, development, testing, and implementation of a specialised web application for assessing the operational, financial, and cybersecurity risks associated with migrating on-premise IT infrastructure to cloud environments. The following boundaries define the scope of the work undertaken. 

In terms of technical scope, the study encompasses the full development lifecycle of a threetier serverless web application: a frontend presentation layer built with HTML5, CSS3, and Vanilla JavaScript; a backend compute layer hosted on AWS Lambda with Python 3.11 runtime, connected to the frontend through AWS API Gateway; and a data persistence layer implemented using Amazon DynamoDB. The risk scoring algorithm, PDF report generation module, and Boto3-based AWS pricing integration are all within scope. 

In terms of cloud platform scope, the system's dynamic, programmatic data retrieval via the Boto3 SDK is scoped exclusively to Amazon Web Services. The system evaluates migration parameters in the context of AWS cloud environments and retrieves real-time pricing data 


from the AWS Price List API. Integration with other cloud providers such as Microsoft Azure or Google Cloud Platform is explicitly out of scope. 

In terms of functional scope, the system is an analytical and decision-support tool. It assesses and quantifies the risks of a proposed migration and generates recommendations for risk mitigation; it does not execute the actual migration of servers, data, or applications. Similarly, while the system generates actionable mitigation recommendations based on identified vulnerabilities, it does not automatically implement or remediate those vulnerabilities within the user's infrastructure. 

In terms of user scope, the system is designed primarily for use by IT project managers, IT auditors, cloud architects, and security professionals who are in the planning or pre-execution phases of a cloud migration project. The system is not designed for use by end-users without a basic understanding of cloud migration concepts. 

In terms of testing scope, the system is validated through unit testing, integration testing, system testing across twenty-five structured scenarios, user acceptance testing with a fivemember evaluator panel, and Apache JMeter performance benchmarking. Testing is confined to the system developed within this study; broader benchmarking against commercial migration tools is not within scope, as that would require access to proprietary tool architectures and commercial licensing. 

## **1.6 Limitations of the Study** 

While this study makes a significant and practical contribution to the field of cloud migration risk management, several limitations must be acknowledged that constrain the generalisability and completeness of the findings. 

First, the system's dynamic pricing integration is limited to Amazon Web Services. The realtime AWS Price List API retrieval via Boto3 ensures that financial risk scores reflect current 


AWS On-Demand pricing but organisations considering migration to Microsoft Azure or Google Cloud Platform cannot rely on the system's financial risk sub-score for accurate cost modeling for those platforms. This single-cloud focus, while a deliberate scope decision, limits the system's applicability for organisations pursuing multi-cloud or non-AWS migration strategies. 

Second, the risk scoring algorithm, while empirically calibrated against authoritative industry data sources, relies on a fixed set of dimension weights and parameter normalisation functions that represent the average risk profile across a broad range of migration contexts. In practice, the risk characteristics of a specific migration may differ significantly from these averages, for example, a highly specialised legacy mainframe migration may present risk patterns that are not well-captured by the algorithm's current parameter taxonomy. While the system allows dimension weights to be adjusted through Lambda environment variables, the core parameter set and normalisation functions are fixed at the time of deployment. 

Third, the user acceptance testing was conducted with a panel of five evaluators, which while sufficient for identifying significant usability issues, is not large enough to generate statistically representative conclusions about the system's usability across the full population of potential users. A larger-scale usability study with a more diverse evaluator population would provide stronger evidence for the system's usability claims. 

Fourth, the system assesses risk based on parameters provided by the user through the input form. The accuracy of the risk assessment is therefore dependent on the accuracy and completeness of the information provided. If a user incorrectly estimates their data volume, misclassifies their data sensitivity, or inaccurately describes their IAM configuration, the resulting risk scores will reflect those inaccuracies. The system does not perform automated discovery of the user's actual infrastructure characteristics; it relies entirely on self-reported parameters. 


Fifth, while the system generates actionable mitigation recommendations, these recommendations are drawn from a fixed knowledge base populated from AWS best practice documentation and established security frameworks. They may not account for organisationspecific constraints, proprietary legacy systems, or highly specialised compliance requirements that fall outside the scope of the standard frameworks consulted. 

## **1.7 Methodology of the Study** 

This study adopts the **Design Science Research (DSR) methodology** as the primary research approach for the design, development, and evaluation of the proposed Cloud Migration Risk Assessment System. Design Science Research is particularly suitable for information systems research because it focuses on the creation of innovative technological artefacts that address identified real-world problems. 

The methodology commenced with an extensive review of literature on cloud computing, cloud migration strategies, IT risk management frameworks, cloud security governance, financial risk modelling, and cloud-native system architectures. The insights obtained from the literature review provided the theoretical foundation for identifying existing gaps in cloud migration risk assessment and informed the design requirements of the proposed system. 

Following the requirements analysis phase, the system architecture was designed using a serverless cloud-native approach based on Amazon Web Services (AWS). The architecture consists of a frontend presentation layer developed using HTML5, CSS3, and JavaScript, a backend processing layer implemented using AWS Lambda and Python, and a data persistence layer implemented using Amazon DynamoDB. 

The development phase adopted Agile software development principles to facilitate iterative implementation, testing, and refinement of system components. The risk scoring engine was designed to evaluate migration projects across three dimensions: operational risk, financial 


risk, and cybersecurity risk. These risk dimensions were subsequently integrated into a composite risk model for overall risk classification. 

The completed system was subjected to comprehensive evaluation through unit testing, 

integration testing, system testing, user acceptance testing, and performance testing to verify its functionality, reliability, security, and usability. 

The methodological process adopted for this study is illustrated in Figure 1.1. 

The adoption of **Design Science Research** ensures that the study not only contributes theoretical knowledge but also produces a practical technological solution to the challenges associated with cloud migration risk assessment. 

## **1.8 Organization of the Study** 

This project report is organised into five chapters, each addressing a specific aspect of the study. 


**Chapter One** presents the introduction to the study. It discusses the background of the study, statement of the problem, aims and objectives, rationale and justification, significance of the study, scope, limitations, methodology, organisation of the study, and definitions of key terms. 

**Chapter Two** provides a comprehensive review of relevant literature relating to cloud computing, cloud migration strategies, cloud security governance, IT risk management frameworks, serverless computing, cloud financial management, and existing cloud migration assessment tools. The chapter also identifies research gaps that justify the development of the proposed system. 

**Chapter Three** describes the methodology and system design adopted for the study. It presents the system architecture, requirements analysis, database design, risk scoring algorithm, API design, security architecture, deployment strategy, and testing methodology used in developing the proposed Cloud Migration Risk Assessment System. 

**Chapter Four** presents the implementation and evaluation of the developed system. It includes screenshots of the user interface, system outputs, testing results, performance evaluation, and analysis of findings obtained during system validation. 

**Chapter Five** presents the summary, conclusion, and recommendations of the study. It highlights the major findings, discusses the contributions of the developed system, identifies limitations, and provides recommendations for future improvements and further research. 

## **1.9 Definitions of Terms** 

The following definitions are provided to ensure clarity and consistency in the interpretation of key terms used throughout this study. 

**Amazon Web Services (AWS)** : A comprehensive and broadly adopted cloud computing platform offered by Amazon, providing over 200 fully featured cloud services including 


computing power, storage, databases, networking, analytics, machine learning, and security tools, delivered from data centres globally. 

**API Gateway** : In the context of this study, AWS API Gateway is a fully managed service that enables developers to create, publish, maintain, monitor, and secure RESTful APIs. It functions as the entry point for client requests to the backend Lambda functions. 

**Audit Trail** : A chronological record of the sequence of activities that have affected, at any time, a specific operation, procedure, event, or device. In this study, an audit trail refers to the immutable DynamoDB records of all completed risk assessments, used to demonstrate compliance and support forensic review. 

**Boto3** : The official AWS Software Development Kit (SDK) for Python, which provides a Pythonic interface to AWS services. In this study, Boto3 is used to programmatically retrieve real-time AWS EC2 pricing data from the AWS Price List API and to interact with Amazon DynamoDB. 

**Capital Expenditure (CapEx)** : Funds used by an organisation to acquire, upgrade, or maintain physical assets such as servers, storage hardware, and network equipment. In the context of on-premise IT, CapEx refers to the large, infrequent investments in infrastructure that are depreciated over time. 

**Cloud Bill Shock** : A colloquial term describing the experience of receiving unexpectedly high cloud computing invoices, typically caused by over-provisioned resources, unanticipated data egress fees, or the uncontrolled consumption of cloud services during or after migration. 

**Cloud Migration** : The process of moving digital assets including applications, data, workloads, and IT processes from on-premise data centres or legacy systems to a cloud computing environment. 


**Composite Risk Score:** The single numerical score produced by the risk scoring algorithm, calculated as a weighted sum of the three dimensional sub-scores (Operational, Financial, and Cybersecurity), expressed on a normalised scale of 0 to 100. 

**DynamoDB** : Amazon DynamoDB is a fully managed, serverless, key-value and document NoSQL database service provided by AWS, designed to deliver single-digit millisecond performance at any scale. In this study, it is used as the audit trail persistence layer. 

**Identity and Access Management (IAM)** : A framework of policies and technologies for ensuring that the right users have the appropriate access to technology resources. In cloud contexts, IAM refers specifically to the configuration of permissions and roles that govern which principals (users, services, or applications) can perform which actions on which cloud resources. 

**Lambda Function** : In the context of AWS Lambda, a function is a unit of code that executes in response to an event trigger. Lambda functions are stateless, short-lived, and automatically scaled by the AWS runtime environment without requiring server provisioning or management. 

**Operational Expenditure (OpEx)** : Ongoing costs for running a product, business, or system. In cloud computing, OpEx refers to the recurring, consumption-based costs of cloud services, which replace the fixed CapEx of on-premise hardware investments. 

**Principle of Least Privilege (PoLP)** : A security concept in which a user, application, or service is granted the minimum level of access or permission needed to perform its intended function. It is considered a foundational best practice in cloud IAM configuration. 

**Risk Score** : A numerical value representing the assessed level of risk associated with a specific dimension or the overall migration project. In this study, risk scores are expressed on a normalised 0 to 100 scale, where higher values indicate greater risk exposure. 


**Serverless Architecture** : A cloud computing execution model in which the cloud provider dynamically manages the allocation and provisioning of servers. Developers deploy code without provisioning or managing any server infrastructure, and are billed only for the actual compute time consumed during execution. 

**Shared Responsibility Model** : A cloud security framework that defines the division of security and compliance responsibilities between the cloud service provider and the cloud customer. The provider is responsible for the security of the underlying cloud infrastructure (hardware, software, networking, and facilities), while the customer is responsible for the security of the applications, data, and configurations deployed within the cloud environment. 

## **CHAPTER TWO** 

## **LITERATURE REVIEW** 

## **2.0 Introduction** 

This chapter provides an extensive and critical review of the existing body of knowledge that informs every design decision embedded in the Cloud Migration Risk Assessment System developed in this study. The review is organised into ten thematic areas: **The Foundational Concepts and Service Models Of Cloud Computing, The Strategic Frameworks and** 


**Well-documented Operational Challenges of Cloud Migration, The Theoretical Basis and Practical Limitations of Established IT Risk Management Methodologies, The Cloud Security Governance Frameworks, Identity Management Paradigms, and** 

**Regulatory Compliance Standards Applicable To Migration Projects, The Financial Dynamics of Transitioning from Capital Expenditure (Capex) to Operational Expenditure (Opex) Cost Models, The Serverless Computing Paradigm and The Specific Characteristics of AWS Lambda, The NoSQL Database Architecture** 

**Underpinning The System's Audit Trail, The Frontend Technologies and Data Visualisation Libraries Employed, A Critical Evaluation Of Existing Commercial and Academic Risk Assessment Tools, and finally, The Synthesis of Identified Gaps that Collectively Justify The System's Design and The Contributions of This Study.** 

By examining each of these areas in depth, this chapter establishes the theoretical and empirical foundations upon which the system's architecture, algorithm design, and evaluation strategy are built. 

## **2.1 Overview of Cloud Computing** 

## **2.1.1 Definition and Essential Characteristics** 

Cloud computing represents a fundamental paradigm shift in the delivery, consumption, and management of information technology resources. Rather than investing in and operating discrete, organisation-owned physical infrastructure, cloud computing allows enterprises to access computing services encompassing servers, storage, databases, networking, analytics, software, and artificial intelligence capabilities on demand, over the internet, paying only for what they consume. 

The National Institute of Standards and Technology (NIST), whose definition is the most widely cited and adopted in both academic and industry discourse, describes cloud computing 


as a model for enabling convenient, on-demand network access to a shared pool of configurable computing resources that can be rapidly provisioned and released with minimal management effort or service provider interaction (Mell & Grance, 2011). This concise definition encapsulates five essential characteristics that collectively distinguish cloud computing from all prior IT delivery models. 

The first essential characteristic is on-demand self-service; a cloud consumer can unilaterally provision computing capabilities such as server time or network storage- as needed, automatically, without requiring human interaction with each service provider. The second is broad network access; capabilities are available over the network and accessed through standard mechanisms that promote use by heterogeneous thin or thick client platforms including mobile phones, tablets, laptops, and workstations. The third is resource pooling; the provider's computing resources are pooled to serve multiple consumers using a multitenant model with different physical and virtual resources dynamically assigned and reassigned according to consumer demand. The fourth is rapid elasticity; capabilities can be elastically provisioned and released- in some cases automatically, to scale rapidly outward and inward commensurate with demand. To the consumer, the capabilities available for provisioning often appear to be unlimited and can be appropriated in any quantity at any time. The fifth is measured service; cloud systems automatically control and optimise resource use by leveraging a metering capability, with resource usage monitored, controlled, and reported in a manner that provides transparency for both the provider and consumer of the utilised service (Mell & Grance, 2011). 

These five characteristics, taken together, explain why cloud computing has supplanted traditional on-premise IT models as the dominant paradigm for enterprise computing. They enable a level of agility, cost-efficiency, and global scalability that was simply not achievable within the confines of organisation-owned data centres. However, they also introduce a 


distinctive set of risks particularly around security, cost management, and operational continuity- that are the subject of this study. 

## **2.1.2 Cloud Service Models** 

Cloud computing is offered through three primary service models, each of which places different security, operational, and financial responsibilities on the consuming organisation, and therefore carries a distinct risk profile that must be accounted for in any comprehensive cloud migration risk assessment framework. 

**Infrastructure as a Service (IaaS)** provides virtualised computing infrastructure including raw processing power, storage capacity, networking, and virtualization (over the internet). In the IaaS model, the cloud provider manages the physical hardware, the virtualisation layer, and the networking infrastructure while the customer is responsible for provisioning and managing virtual machines, operating systems, middleware, runtime environments, data, and applications. Amazon EC2, Microsoft Azure Virtual Machines, and Google Compute Engine are leading IaaS offerings. IaaS provides maximum flexibility and control but imposes the highest customer responsibility for security and operational management (Bhardwaj et al., 2010). 

**Platform as a Service (PaaS)** abstracts the underlying infrastructure further- providing a managed environment in which developers can build, deploy, test, and manage applications without concerning themselves with the provisioning or management of servers, storage, or operating systems. The provider manages the infrastructure, operating systems, middleware, and runtime environments; the customer manages applications and data. AWS Elastic Beanstalk, Google App Engine, and Microsoft Azure App Service are widely used PaaS platforms. PaaS reduces operational burden but constrains the customer's control over the underlying execution environment, introducing a different class of dependency risk. **Software as a Service (SaaS)** represents the highest level of abstraction, delivering fully 


managed, ready-to-use software applications over the internet. In the SaaS model, the provider manages the entire technology stack- infrastructure, platforms, applications, and data management while the customer accesses the application through a web browser or API. Microsoft 365, Google Workspace, Salesforce, and ServiceNow are archetypal SaaS offerings. SaaS eliminates infrastructure management overhead entirely but provides the least control over data residency, security configuration, and application architectureconsiderations of particular importance for organisations subject to strict data sovereignty regulations. 

## **2.1.3 Cloud Deployment Models** 

Cloud environments are further classified by deployment model, each representing a different balance between control, scalability, and cost efficiency. A public cloud is operated by a thirdparty provider and delivers services over the internet to multiple customers who share the same underlying physical infrastructure, benefiting from massive economies of scale and a pay-as-you-go financial model. A private cloud is provisioned exclusively for a single organization- either on-premise within the organisation's own data centre or in a dedicated, hosted environment offering greater control, customisation, and data sovereignty at the cost of reduced scalability and higher operational overhead. A hybrid cloud combines elements of both models; enabling organisations to retain sensitive or regulated workloads on-premise or in a private cloud while leveraging the scalability and cost-efficiency of the public cloud for less sensitive, variable, or burst workloads (Buyya et al., 2009). A community cloud is a less common deployment model in which infrastructure is shared among several organisations with common concerns such as regulatory compliance or mission and may be managed by the organisations themselves, a third party, or a combination. The risk assessment system developed in this study is designed primarily for the most commercially prevalent and 


operationally complex migration scenario: the transition from on-premise private infrastructure to a public cloud environment hosted on Amazon Web Services. 

|||||<br>|
|---|---|---|---|---|
|**Service Model**|**Customer Manages**|**Provider Manages**|**Risk Profile**||
||||||
|IaaS|OS,<br>middleware,<br>runtime, data,<br>applications|Hardware,<br>virtualisation,<br>networking, storage|High operational &<br>security responsibility||
||Applications, data|OS,<br>middleware,<br>runtime, infrastructure|<br> <br>Medium; dependency<br>on<br>platform<br>configurations||
|PaaS|||||
||||||
|SaaS|User<br>access,<br>data<br>governance|<br>Everything (infra to<br>application)|Low operational; high<br>data sovereignty risk||



**Table 2.1: Cloud Service Model Comparison and Associated Risk Profiles** 

## **2.2 Cloud Migration: Concepts, Strategies, and Challenges** 

## **2.2.1 Defining Cloud Migration** 

Cloud migration is the process of moving an organisation's digital assets- encompassing applications, databases, workloads, IT processes, and in many cases entire operating 


environments, from on-premise data centres or legacy computing systems to a cloud computing environment. It is crucial to understand from the outset that cloud migration is not a discrete, atomic event but a complex, iterative, and phased undertaking that may span months or years depending on the size, heterogeneity, and interdependence of the systems being migrated. The complexity of this undertaking is compounded by the fundamental heterogeneity of enterprise IT environments which typically includes a mixture of legacy applications with undocumented dependencies, proprietary hardware configurations, tightly coupled data pipelines, and bespoke integration layers accumulated over decades of IT investment. As a consequence, straightforward, like-for-like migration- simply moving an application from a physical server to a virtual machine in the cloud without modification is extremely rare for production enterprise workloads. Almost every meaningful enterprise migration requires some degree of adaptation, re-engineering, or re-architecting of existing systems to function correctly, securely, and cost-efficiently in the cloud environment (Gartner, 2019). 

## **2.2.2 The 6Rs Migration Strategy Framework** 

Gartner introduced the concept of the '5 Rs' of cloud migration to provide a structured taxonomy of the strategic approaches available to organisations migrating workloads to the cloud. Amazon Web Services subsequently expanded this taxonomy to the '6 Rs' to account for the full breadth of real-world migration scenarios encountered in enterprise practice. 

These six strategies represent the spectrum of possible migration approaches, ranging from the minimum-modification lift-and-shift at one extreme to the complete decommissioning of obsolete workloads at the other. Understanding which strategy is appropriate for a given workload and the specific risk implications of that choice is a foundational analytical task in cloud migration planning - and a key function of the risk scoring system developed in this study. 

|**Strategy**|**Common Name**|**Description**|**Risk Level**<br>**Complexity**|**Risk Level**<br>**Complexity**|
|---|---|---|---|---|
|||||Low|
||||||




||||||
|---|---|---|---|---|
|Refactoring|Re-architecting|Redesign as cloudnative<br>microservices<br>or<br>serverless|<br> <br>High|Very High|
||||Very Low<br> <br>|Very Low|
|Retiring|Decommissioning|<br>Identify and eliminate<br>applications no longer<br>needed|||
||||||
|Retaining|Revisit Later|Keep<br>certain<br>apps<br>onpremise due to<br>constraints|<br>Low|Low|
|Rehosting|Lift and Shift|Move applications asis<br>without<br>modification<br>to cloud VMs|Low-<br>Medium||
||||||
|Replatforming|Lift, Tinker and<br>Shift|Minor<br>cloud<br>optimisations without<br>core architecture change|<br> <br>Medium|Low-<br>Medium|
||||Medium|Low|
|Repurchasing|Drop and Shop|Replace<br>on-prem<br>software with SaaS<br>equivalent|||




## **Table 2.2: The 6Rs Cloud** 

## **Migration Strategy Framework with Risk and Complexity Profiles** 

**Rehosting** , commonly referred to as 'lift and shift', involves migrating applications to the cloud as-is-  without any modification to the application code, configuration, or architecture. Rehosting is typically the fastest and lowest-complexity approach, requiring minimal cloud expertise and producing the shortest migration timelines. However, it also produces the smallest long-term efficiency gains; a workload that is simply rehosted in the cloud without optimisation often costs more to run in the cloud than it did on-premise, because it does not take advantage of cloud-native capabilities such as auto-scaling, managed services, or reserved pricing models (Gartner, 2019). 

**Replatforming** makes limited optimisations to exploit cloud capabilities. For example, migrating an on-premise relational database to a managed cloud database service- without changing the core application architecture. This approach offers a better balance between migration speed and cloud efficiency than pure rehosting. 

**Refactoring** , or re-architecting, involves fundamentally redesigning applications to be cloudnative often decomposing monolithic applications into microservices, adopting containerisation, or rebuilding as serverless functions. This strategy delivers the greatest longterm efficiency, scalability, and cost optimisation, but it introduces the highest implementation complexity, the longest migration timelines, the greatest risk of project overruns, and demands the deepest cloud-native expertise from the development team. 

## **2.2.3 The Challenge of Application Dependency Mapping** 

One of the most pervasive and consistently underestimated challenges in enterprise cloud migration is the accurate identification and documentation of application dependencies; the network of relationships between applications, databases, middleware components, APIs, and 


infrastructure elements that must function correctly in concert for a given application to operate as intended. In many enterprise environments, particularly those that have evolved organically over long periods, application dependencies are poorly documented or entirely undocumented, meaning that the full dependency graph of a given system can only be discovered through runtime network traffic analysis, agent-based infrastructure discovery, or direct interrogation of application owners (Jamshidi et al., 2013). The failure to accurately map application dependencies before migration is a leading cause of post-migration failures; applications that function correctly in isolation may fail catastrophically when separated from dependent services that have not yet been migrated, or when the network latency between them increases as a consequence of geographic separation in the cloud. The migration complexity parameter captured in the risk assessment system developed in this study directly quantifies the assessed complexity of an organisation's application dependency landscape, and this parameter carries a weight of 30% in the Operational Risk sub-score- reflecting the central importance of dependency management to migration success. 

## **2.2.4 Data Gravity and Transfer Challenges** 

The concept of data gravity first articulated by Dave McCrory (2010) describes the tendency of large datasets to attract and accumulate dependent services, applications, and processing workloads, creating a form of organisational inertia that makes these datasets difficult and expensive to move. For organisations with very large data estates- multiterabyte or petabytescale datasets; data gravity presents a fundamental migration challenge; the physical transfer of large volumes of data to the cloud can take days or weeks over standard internet connections, during which time data consistency must be maintained between the source and target environments. AWS offers services such as AWS Snowball- a petabyte-scale physical data transfer device, and AWS DataSync- a managed online data transfer service to address this challenge, but the logistical complexity and the risk of data loss or corruption during 


transfer remain significant. The data volume parameter in the Operational Risk sub-score of this study's algorithm directly addresses this dimension of migration risk, with larger data volumes mapped to higher operational risk contributions using a piecewise linear normalisation function calibrated against IDC migration scale classifications. 

## **2.2.5 Documented Financial Consequences of Migration Failures** 

The financial consequences of cloud migration failures are well-evidenced in industry research. The IDC (2019) study of enterprise cloud migration outcomes found that unplanned downtime during cloud migration costs enterprises an average of $250,000 per hour, with the most severe incidents costing well in excess of $1 million per hour for largescale e-commerce or financial services platforms. The Ponemon Institute (2022) reported that the average total cost of a data breach- many of which originate from cloud misconfiguration errors introduced during or after migration, stands at $4.35 million globally, rising to $9.44 million for organisations in the United States healthcare sector. The Flexera State of the Cloud Report (2023) found that organisations waste an average of 32% of their total cloud spending- a direct consequence of inadequate pre-migration financial modelling, over-provisioning of cloud resources, and the accumulation of orphaned resources that are no longer in use but continue to accrue charges. These statistics collectively underscore the high-stakes nature of cloud migration as an enterprise undertaking and the critical importance of rigorous, datadriven risk assessment before migration activities commence. 

## **2.3 IT Risk Management Frameworks** 

## **2.3.1 Foundational Principles of IT Risk Management** 

Risk management in the context of information technology projects is the structured, systematic process of identifying, assessing, and responding to risks that could adversely affect the achievement of project objectives within the bounds of cost, schedule, scope, and 


quality. The ISO 31000:2018 Risk Management standard- the international standard for risk management principles and guidelines, defines risk as 'the effect of uncertainty on objectives', and risk management as the coordinated activities undertaken to direct and control an organisation with regard to risk. In the context of IT projects, risk management encompasses four sequential but iterative activities; Risk Identification which involves the comprehensive cataloguing of all events or conditions that could adversely affect project outcomes, Risk Assessment which involves evaluating the likelihood and potential impact of each identified risk, Risk Response Planning that involves developing strategies to reduce the probability or impact of risks deemed unacceptable, and Risk Monitoring And Control which involves continuously tracking identified risks, identifying new risks, and evaluating the effectiveness of response strategies throughout the project lifecycle (ISO, 2018). 

Several established frameworks provide structured guidance for IT risk management practice. NIST Special Publication 800-30 (Guide for Conducting Risk Assessments) provides a systematic, repeatable methodology for evaluating the risks associated with information systems, incorporating threat identification, vulnerability assessment, impact analysis, and risk determination. COBIT 5 (Control Objectives for Information and Related Technologies), published by ISACA, provides a comprehensive governance and management framework for enterprise IT that includes detailed risk management guidance integrated with business objectives and compliance requirements. The Project Management Institute's PMBOK Guide identifies risk management as one of ten core project management knowledge areas, encompassing risk planning, identification, qualitative analysis, quantitative analysis, response planning, and monitoring and control. The Factor Analysis of Information Risk (FAIR) model provides a quantitative approach to cybersecurity risk analysis by decomposing risk into its constituent factors; threat event frequency, threat capability, 


vulnerability, and loss magnitude- and modelling their interactions using probabilistic methods. 

## **2.3.2 Qualitative versus Quantitative Risk Assessment** 

IT risk management methodologies can be broadly categorised as either qualitative or quantitative, with each approach offering distinct advantages and limitations that determine its suitability for different risk assessment contexts. Qualitative risk assessment methods assign descriptive, categorical ratings typically expressed as High, Medium, or Low- to risk likelihood and impact, producing a probability-impact matrix that allows risks to be prioritised and categorised. Qualitative methods are widely adopted in practice because they are straightforward to apply, require no specialised statistical expertise, and are broadly comprehensible to non-technical stakeholders. However, they are fundamentally limited by their reliance on subjective expert judgment; different assessors will often assign different ratings to the same risk, producing inconsistent and potentially misleading results. Qualitative ratings also lack the numerical precision required for financial forecasting, executive reporting, or regulatory compliance documentation. 

Quantitative Risk Assessment (QRA) methods apply numerical values to risk likelihood and impact, producing objective, comparable, and financially meaningful risk evaluations. Common QRA techniques include Monte Carlo simulation which uses statistical sampling to model the probability distribution of possible project outcomes and quantify the range of potential financial losses, Expected Monetary Value (EMV) analysis which calculates the average outcome of uncertain decisions by weighting possible outcomes by their probability, and established vulnerability scoring systems such as the Common Vulnerability Scoring System (CVSS) which assigns standardised numerical severity scores to software 

vulnerabilities based on their exploitability, scope of impact, and potential consequences. The risk scoring algorithm developed in this study is grounded in quantitative risk assessment 


principles; it assigns empirically calibrated numerical weights to migration parameters across three risk dimensions and computes a composite risk score on a 0-to100 normalised scale, providing a single, objective, and financially interpretable measure of a proposed migration's risk exposure. 

## **2.3.3 The Structural Limitations of Static Risk Registers** 

Despite the widespread acknowledgement of quantitative risk assessment's superiority for complex, high-stakes projects, the static risk register remains the dominant risk management tool in enterprise IT project management practice. A risk register is a document- typically maintained in spreadsheet form that catalogues identified project risks, assigns qualitative likelihood and impact ratings to each risk, describes planned mitigation and response strategies, and designates a risk owner responsible for monitoring and managing each risk. Risk registers are universally required by established project management methodologies including PRINCE2 and PMI's PMBOK and they provide a valuable baseline framework for risk identification and categorisation. However, for cloud migration projects specifically, static risk registers exhibit a set of fundamental structural limitations that render them demonstrably inadequate as the primary risk assessment mechanism. 

The most fundamental limitation of the static risk register is that it is a snapshot document; it captures the state of identified risks at a particular moment in time and is typically updated only at fixed project milestones often no more frequently than weekly or fortnightly. In cloud environments, where configurations can be changed in seconds, pricing models are updated without notice, and new security vulnerabilities are disclosed daily, a risk register that was accurate at the time of its creation may be dangerously outdated by the time the migration team acts on it. Bannerman (2008) demonstrated in a longitudinal study of IT project risk management practices that risk registers are often maintained as compliance artefacts- created to satisfy governance requirements at project initiation rather than as living decision-support 


tools that are actively maintained and consulted throughout the project lifecycle. This finding, replicated in subsequent studies by Kutsch and Hall (2010), suggests that the widespread adoption of risk registers does not necessarily translate into effective, real-time risk management in practice. 

A second critical limitation is the qualitative, subjective nature of the ratings assigned in most risk registers. The assignment of a 'High', 'Medium', or 'Low' likelihood or impact rating to a cloud migration risk is inherently subjective, varies significantly between assessors, and cannot be readily translated into quantitative financial estimates or compared objectively across different risks or different migration projects. This qualitative imprecision makes it impossible to accurately prioritise mitigation resource allocation, produce financially credible risk-adjusted cost forecasts for executive leadership, or demonstrate the quantitative rigour expected by regulatory auditors assessing compliance documentation. Most critically, static risk registers cannot integrate with live data sources; they cannot query real-time cloud pricing APIs to reflect current cost models, nor can they programmatically evaluate a specific proposed cloud configuration against current security compliance benchmarks. The result is a persistent and dangerous gap between the static risk picture presented in the register and the dynamic continuously evolving reality of the cloud environment being assessed. 

|||||
|---|---|---|---|
|**Limitation**||**Impact**<br>**on**<br>**Cloud**|<br>**System's Resolution**|
|||||
|||**Migration**||
|||||
|||||
|Point-inonly<br>napshot||<br>Risk<br>assessments|Real-time API-driven scoring at each|
||||assessment submission|
|||become outdated rapidly||
|||in<br>dynamic<br>cloud||
|||environments||
|||||
|||||




|||||
|---|---|---|---|
|Qualitative<br>only<br>ratings||Cannot<br>support<br>financial<br>forecasting<br>or<br>regulatory<br>quantification|0-to-100<br>composite<br>score<br>with<br>dimensional sub-scores|
|||||
|No<br>live<br>integration<br>data||<br>Financial risk scores based|Boto3 AWS Pricing API integration for|
|||on static, outdated pricing|real-time cost data|
|||tables||
|||||
|||||
|No<br>security<br>evaluation<br>config||Cannot<br>assess<br>specific<br>IAM/encryption<br>configurations<br>against<br>benchmarks|IAM permissiveness and encryption<br>parameters as scored inputs|
|||||
|Manual<br>required<br>update||<br>Register rapidly becomes|Automated<br>scoring  on<br>demand;|
|||stale<br>without<br>disciplined||
|||<br>maintenance|DynamoDB immutable audit trail|
|||||
|||||
|No<br>composite<br>metric<br>risk||<br>Cannot<br>communicate<br>unified<br>risk<br>posture<br>executive stakeholders<br>a<br>to|<br>Single composite score on 0-100 scale<br>with colour-coded tier|



**Table 2.3: Structural Limitations of Static Risk Registers and the System's** 

**Resolutions** 

## **2.4 Cloud Security Governance** 

## **2.4.1 The Shared Responsibility Model in Depth** 


The Shared Responsibility Model is the foundational security governance framework that defines how security and compliance obligations are divided between cloud service providers and their customers. In the AWS implementation of this model- the most comprehensively documented and widely adopted version, the division of responsibility is expressed through the distinction between 'security of the cloud' and 'security in the cloud'. AWS is responsible for the security of the cloud; the physical security of its global data centre facilities, the integrity and security of the hardware infrastructure (servers, storage, networking equipment), the managed hypervisor layer, and the security of AWS-managed services including their underlying operating systems and network infrastructure. The cloud customer, by contrast, is entirely responsible for security in the cloud: the configuration of every resource they deploy within the AWS environment, the classification and protection of their data, the management of user identities and access permissions, the security configuration of their operating systems and network controls, the encryption of data in transit and at rest, and the security of the applications they build and deploy on AWS infrastructure (AWS, 2023). 

This division of responsibility represents a significant and frequently misunderstood paradigm shift for organisations transitioning from on-premise environments. In a traditional on-premise data centre, the organisation's IT security team controlled every layer of the security stack- from physical facility security to application-level controls; creating a clear, unified locus of security accountability. In the cloud, by contrast, the customer's security perimeter becomes defined not by the physical boundaries of a network, but by the correctness and completeness of the configuration choices made for every deployed cloud resource. A single misconfiguration- an overly permissive IAM policy, a publicly exposed storage bucket, an unencrypted database instance can expose an entire organisation's data estate to external actors. The proposed risk assessment system explicitly evaluates the user's stated security configuration against Shared Responsibility compliance benchmarks, 


generating targeted priority alerts for configurations that fall short of the customer's cloud security obligations. 

## **2.4.2 Identity and Access Management Risks** 

Identity and Access Management (IAM) is the technical mechanism through which organisations control which users, services, and applications can access cloud resources and perform which operations on those resources. In AWS, IAM enables the definition of granular, policy-based access controls expressed in JSON-formatted policy documents that specify, at the level of individual API actions and individual resources, exactly which principals (users, roles, or services) may perform which operations under which conditions. When configured correctly- adhering to the Principle of Least Privilege, which mandates that each principal is granted only the minimum permissions required to perform its intended function, AWS IAM provides a powerful mechanism for limiting the potential damage caused by compromised credentials, insider threats, or misconfigured services. 

However, IAM is frequently and consequentially misconfigured in practice. The most dangerous IAM misconfigurations identified in industry research include; the use of wildcard permissions (using 'Action': '*' and 'Resource': '*' in IAM policy documents) that grant a principal unrestricted access to all AWS services and resources, the failure to enforce multifactor authentication for privileged user accounts, the creation of IAM access keys with excessive privileges that are not rotated on a regular schedule and not deactivated when no longer needed, the use of the AWS root account for day-to-day operations rather than purpose-created IAM roles with appropriately scoped permissions, and the use of overly broad, pre-defined AWS managed policies (such as AdministratorAccess) in contexts where more granular, least-privilege policies would be appropriate (Cloud Security Alliance, 2022). The Cloud Security Alliance (CSA) consistently identifies IAM misconfigurations as one of the top threats to cloud security in its annual Top Threats to Cloud Computing report. The 


risk scoring system developed in this study incorporates IAM permissiveness as a highweight input parameter (weight: 0.30) in the Cybersecurity risk sub-score, reflecting the central importance of access control configuration in determining the security posture of a cloud deployment. 

## **2.4.3 Encryption and Data Protection Requirements** 

Encryption is the process of transforming data into an unintelligible format using a cryptographic algorithm, such that only authorised parties possessing the correct decryption key can recover the original data. In cloud computing contexts, encryption is required both for data in transit; data moving between a client and a cloud service, or between cloud services and for data at rest- data stored in cloud databases, object storage systems, or file systems. Failure to encrypt data appropriately in cloud environments creates significant risk; data traversing network connections without encryption can be intercepted by adversaries conducting man-in-the-middle attacks; data stored without encryption can be accessed by cloud provider employees, compromised by storage layer vulnerabilities, or exposed in the event of a misconfiguration that grants unintended access to storage resources. 

AWS provides comprehensive encryption capabilities at every layer of its service stack, including TLS 1.2 and 1.3 for data in transit, AWS Key Management Service (KMS) for centralised management of encryption keys for data at rest, and server-side encryption for 

AWS storage services including S3, EBS, and RDS. Regulatory frameworks including GDPR Article 32, HIPAA Technical Safeguard provisions, and PCI DSS Requirement 3 mandate the use of strong encryption for specified categories of data, making encryption posture a direct determinant of regulatory compliance status in cloud environments. The encryption parameter in the Cybersecurity risk sub-score of this study's algorithm (weight: 0.20) captures the assessed quality of a proposed migration's encryption posture across these dimensions. 


## **2.4.4 Regulatory Compliance Frameworks Applicable to Cloud Migrations** 

|||||
|---|---|---|---|
|**Framework**|**Jurisdiction**<br>**/**<br>**Sector**|<br>**Key**<br>**Cloud**<br>**Requirements**|<br>**Non-Compliance**<br>**Consequences**|
|||||
|GDPR|EU- all sectors<br>handling<br>EU<br>personal data|<br>Data<br>minimisation,<br>encryption at rest/transit,<br>breach notification <72hrs,<br>data residency controls|<br>Fines up to 4% of global<br>annual turnover or €20M|
|HIPAA|US- Healthcare|||
|||Access controls, audit<br>controls, encryption of<br>PHI, risk analysis<br>documentation|Civil penalties up to $1.9M<br>per violation<br>category per year|
|||||
|PCI DSS v4.0|Global-<br>Payment<br>card processing|<br>Network<br>segmentation,<br>encryption of cardholder<br>data, access control,<br>penetration testing|Loss of card processing<br>rights, fines up to<br>$100k/month|
|SOX|US-<br>Listed<br>companies|<br>IT controls for financial<br>data integrity, access logs,<br>change management|<br>Criminal  penalties<br>for<br>executives; delisting|
|||||
|ISO 27001|Global- all sectors|<br>ISMS implementation,<br>risk assessment, asset<br>management,<br>incident<br>management|Loss  of<br>certification;<br>contractual impacts|
|||||




|NIST CSF<br>US-<br>Critical<br>infrastructure<br>Identify, Protect, Detect,<br>Respond,<br>Recover<br>functions<br>Regulatory<br>and<br>reputational consequences|NIST CSF<br>US-<br>Critical<br>infrastructure<br>Identify, Protect, Detect,<br>Respond,<br>Recover<br>functions<br>Regulatory<br>and<br>reputational consequences|NIST CSF<br>US-<br>Critical<br>infrastructure<br>Identify, Protect, Detect,<br>Respond,<br>Recover<br>functions<br>Regulatory<br>and<br>reputational consequences|NIST CSF<br>US-<br>Critical<br>infrastructure<br>Identify, Protect, Detect,<br>Respond,<br>Recover<br>functions<br>Regulatory<br>and<br>reputational consequences|NIST CSF<br>US-<br>Critical<br>infrastructure<br>Identify, Protect, Detect,<br>Respond,<br>Recover<br>functions<br>Regulatory<br>and<br>reputational consequences|
|---|---|---|---|---|
||NIST CSF|US-<br>Critical<br>infrastructure|<br>Identify, Protect, Detect,<br>Respond,<br>Recover<br>functions|<br>Regulatory<br>and<br>reputational consequences|



**Table 2.4: Regulatory Compliance Frameworks and Their Cloud Security** 

## **Requirements** 

## **2.5 Financial Risk and Cloud Cost Management** 

## **2.5.1 The CapEx-to-OpEx Transition in Depth** 

The most significant and potentially destabilising financial implication of cloud migration is the fundamental restructuring of how IT costs are incurred, categorised, and managed across the organisation's financial operations. In traditional on-premise IT environments, organisations make large, infrequent capital investments in physical servers, storage systems, networking equipment, software licences, and data centre facilities. These expenditures are classified as Capital Expenditures (CapEx), meaning they are recorded on the organisation's balance sheet as the acquisition of long-term assets, and their cost is amortised through depreciation charges spread across the useful life of the asset- typically three to five years for IT hardware. This model, while requiring significant upfront investment, provides a high degree of financial predictability: once the hardware is purchased and deployed, the IT team knows precisely what computing capacity they have, when the next refresh cycle will be required, and what the annual depreciation charge will be. This predictability makes IT costs straightforward to budget and model within conventional multiyear financial planning cycles. 

In the cloud, this model is replaced by an Operational Expenditure (OpEx) model in which computing resources are consumed as a metered service and billed based on actual usage at a granularity of per-second, per-request, per-gigabyte, or per-API-call depending on the service. This billing model offers substantial advantages in capital efficiency- organisations 


avoid large upfront hardware investments, do not maintain costly excess capacity to handle peak demand, and can scale their infrastructure precisely to match workload demand at any point in time. However, the OpEx model introduces significant financial forecasting complexity that organisations transitioning from on-premise environments are frequently unprepared to manage. Cloud costs can fluctuate dramatically based on usage patterns, seasonal demand variation, data transfer volumes between services and regions, and the configuration choices made for specific cloud services. Without disciplined cost governance and proactive financial modelling, cloud costs can escalate rapidly and unpredictably therefore producing the phenomenon widely known in the industry as 'cloud bill shock'. 

## **2.5.2 Sources of Cloud Financial Risk** 

Research by the Flexera State of the Cloud Report (2023) identified that organisations waste an average of 32% of their total cloud spend- representing billions of dollars of unnecessary expenditure globally per year. The principal sources of cloud financial waste identified in this and related studies include; over-provisioning of compute resources, where virtual machine instances are sized based on peak theoretical demand rather than actual average utilisation, resulting in chronically underutilised resources that accrue charges continuously; orphaned resources, including unattached storage volumes, idle load balancers, and inactive database instances, that continue to accrue charges after the workloads they supported have been terminated or migrated; unanticipated data egress fees, where the cost of transferring data out of the cloud to on-premise systems, to end users, or between cloud regions is not factored into pre-migration financial models; runaway auto-scaling, where auto-scaling configurations trigger the provisioning of additional compute capacity in response to traffic spikes or load testing events, resulting in temporarily very high costs that were not anticipated; and the accumulation of development and testing environments that are deployed for temporary use but inadvertently left running in production. 


The risk assessment system developed in this study addresses this financial risk dimension by incorporating three financial parameters- projected monthly resource cost (dynamically computed using live AWS pricing), data egress volume, and the CapEx-to-OpEx transition delta into the Financial Risk sub-score computation. The use of real-time AWS pricing data via the Boto3 SDK ensures that financial risk scores reflect current market rates rather than the static pricing snapshots that rapidly become outdated as AWS adjusts its pricing on an ongoing basis. 

## **2.5.3 The FinOps Discipline** 

In response to the widespread challenge of cloud cost management, the Cloud Financial Management discipline commonly referred to as FinOps has emerged as a structured approach to managing cloud spending that bridges the gap between engineering, finance, and business operations. The FinOps Foundation (2023) defines FinOps as 'an evolving cloud financial management discipline and cultural practice that enables organisations to get maximum business value by helping engineering, finance, and technology teams collaborate on data-driven spending decisions.' The FinOps lifecycle comprises three iterative phases; Inform which involves establishing real-time visibility into cloud costs and usage across all teams, Optimise which involves identifying and implementing opportunities to eliminate waste and right-size resources, and Operate which involves embedding cost accountability into continuous organisational processes and governance structures. The risk assessment system developed in this study contributes directly to the Inform phase of premigration FinOps practice by programmatically modelling projected resource costs against real-time AWS pricing data, providing organisations with a financially grounded risk quantification before any cloud resource commitments are made. 

## **2.6 Serverless Computing and AWS Lambda** 


## **2.6.1 The Serverless Paradigm** 

Serverless computing is a cloud execution model in which the cloud provider dynamically manages all aspects of server provisioning, scaling, patching, and maintenance, allowing developers to focus exclusively on writing and deploying application logic without managing any underlying server infrastructure. Despite the somewhat misleading name, physical servers are still involved from the developer's perspective, the server layer is entirely abstracted away; developers write discrete, event-triggered functions and deploy them to the cloud, where the provider handles all aspects of execution environment management. The serverless model is characterised by event-driven execution, where function instances are invoked in response to triggers such as HTTP requests, database change events, or scheduled timer events; automatic scaling, where the cloud platform provisions as many parallel function instances as required to handle concurrent invocations without any manual capacity planning; and consumption-based billing, where charges accrue only for the actual compute time consumed during each function execution, with no charges for idle time between invocations (Roberts, 2018). 

The serverless model offers two key properties that make it particularly well-suited for the backend API of the risk assessment system developed in this study. First, automatic scaling; the AWS Lambda runtime automatically provisions additional concurrent execution environments in response to increasing request volumes, ensuring that the system can handle bursts of concurrent assessment requests from multiple users without any manual intervention or capacity provisioning. This scalability is directly aligned with NFR-2 (Scalability), which requires automatic horizontal scaling to accommodate concurrent assessment requests. Second, the elimination of server management overhead, which removes an entire category of operational risk and reduces the total cost of system ownership to near-zero outside of actual usage periods. 


## **2.6.2 AWS Lambda Technical Architecture** 

AWS Lambda, launched by Amazon Web Services in November 2014, is the most widely adopted Function-as-a-Service (FaaS) platform, processing trillions of function invocations monthly across millions of customer deployments. Lambda enables developers to run code in response to events such as HTTP requests routed through API Gateway, messages published to Amazon SQS, or files uploaded to Amazon S3 without provisioning or managing any underlying server infrastructure. Lambda functions are defined by three core properties; the function code, which contains the application logic and is packaged as a deployment package or container image, the execution role, an IAM role that defines what AWS resources and services the function is permitted to interact with, and the runtime environment, which specifies the programming language and version used to execute the function (AWS, 2023). Lambda supports runtimes for Python, Node.js, Java, Go, Ruby, and .NET, as well as custom runtimes for any language that can be compiled to run on Amazon Linux. Python 3.11 is selected for the backend Lambda functions in this system because of its rich ecosystem of data processing and cloud computing libraries, including Boto3- the official AWS SDK for Python which is central to the real-time pricing integration functionality. 

A characteristic of Lambda deployments that requires careful architectural consideration is the cold start phenomenon- when a Lambda function is invoked after a period of inactivity, or when the platform scales out to handle increased concurrency, it must initialise a new execution environment- downloading the function's deployment package, initialising the runtime, and running any initialisation code outside the handler function. This initialisation process introduces additional latency on the first invocation after a cold start period, typically ranging from a few hundred milliseconds to several seconds depending on the function's package size, runtime, and initialisation complexity. Leitner et al. (2019) conducted an empirical study of Lambda cold start performance across multiple runtimes and found that 


Python functions exhibit among the shortest cold start latencies, typically between 100ms and 400ms, making Python the optimal runtime choice for latency-sensitive API backends. The system's performance requirement (NFR-1: response within three seconds) accounts for this cold start overhead, and the Apache JMeter performance benchmarking described in Section 3.9.5 validates that the system meets this requirement under realistic concurrent load conditions. 

## **2.6.3 AWS API Gateway** 

AWS API Gateway is a fully managed service that enables developers to create, publish, maintain, monitor, and secure RESTful and WebSocket APIs at any scale. It acts as the architectural front door for backend services in this system, the Lambda functions- handling all aspects of HTTP traffic management including request routing, input validation, authorisation enforcement, request throttling, SSL/TLS termination, and Cross-Origin Resource Sharing (CORS) configuration. API Gateway integrates natively with AWS Lambda through a Lambda Proxy Integration, which passes the complete HTTP request event including the request path, HTTP method, query string parameters, request headers, and body to the Lambda function as a structured JSON event object, and returns the Lambda function's structured JSON response as the HTTP response. This integration pattern enables the construction of fully serverless API backends with zero infrastructure management overhead, built-in DDoS protection through AWS Shield integration, and automatic scaling to handle millions of concurrent API requests. 

## **2.7 Amazon DynamoDB and NoSQL Database Architecture** 

Amazon DynamoDB is a fully managed, serverless NoSQL key-value and document database service designed to deliver single-digit millisecond read and write performance at any scale. Unlike traditional relational database management systems, which organise data in structured 


tables with fixed schemas enforced through primary key and foreign key constraints, DynamoDB uses a flexible, schema-less data model in which each item (analogous to a row in a relational database) can have a different set of attributes, and the schema can evolve over time without requiring database schema migrations. Data in DynamoDB is organised into tables, with each item identified by a primary key that may be a simple partition key or a composite partition key plus sort key. 

DynamoDB's serverless billing model- where charges accrue based on the number of read and write request units consumed, with no charges for idle capacity aligns directly with the overall serverless architecture of the risk assessment system and eliminates the need for capacity planning. Its native integration with AWS IAM enables fine-grained, attributelevel access control for Lambda function execution roles. Its immutable write semantics enforced through IAM restrictions that prevent the system's Lambda execution roles from issuing UpdateItem or DeleteItem operations- satisfy the audit trail integrity requirements for compliance reporting. Point-in-Time Recovery (PITR) is enabled on the DynamoDB table, providing continuous backup with a 35-day recovery window- a critical capability for compliance-regulated industries that require data retention and recovery capabilities. 

## **2.8 Frontend Technologies and Data Visualisation** 

The frontend dashboard of the proposed system is constructed using the foundational technologies of the web platform: HTML5 for content structure and semantic markup, CSS3 for visual styling and responsive layout, and Vanilla JavaScript (ES6+)- the standardised, framework-free implementation of the JavaScript language (for dynamic behaviour, asynchronous API communication, and interactive visualization). The deliberate choice of Vanilla JavaScript over modern framework ecosystems such as React, Angular, or Vue.js reflects an architectural prioritisation of performance, maintainability, and portability over framework-specific development convenience. Heavy JavaScript frameworks impose 


significant runtime overhead in the form of large bundle sizes that increase initial page load times, complex build pipeline dependencies that add maintenance burden, and framework version lifecycle management challenges that create long-term technical debt. For a dashboard application that serves a technically sophisticated audience of project managers and IT auditors- and that prioritises rapid load times, broad browser compatibility without transpilation, and minimal external dependency footprint, the Vanilla JavaScript approach provides the full expressive capability required through native browser APIs without the overhead imposed by framework runtimes. 

Chart.js v4.x is employed for data visualisation. It is a mature, actively maintained, opensource JavaScript charting library that renders visualisations on HTML5 Canvas elements, supporting a comprehensive range of chart types including radar charts, doughnut charts, bar charts, and line charts, all with built-in animation, responsive sizing, and interactive tooltip support. For the risk assessment dashboard, Chart.js renders two primary visualisations; a radar chart that plots the three normalised sub-scores- Operational, Financial, and Cybersecurity on equidistant axes, enabling immediate visual comparison of relative risk exposure across the three dimensions, and a doughnut gauge representing the composite risk score on a 0-to-100 scale, colour-coded by risk tier (green for Low, amber for Medium, red for High). Both visualisations update dynamically upon receipt of each API response without requiring a page reload, providing users with immediate visual feedback on the risk profile of each submitted scenario. 

## **2.9 Review of Existing Cloud Migration Risk Assessment Tools** 

## **2.9.1 Commercial Assessment Tools** 

Several commercial tools have been developed to support cloud migration planning, infrastructure discovery, and cost modelling. AWS Migration Evaluator (formerly TSO 


Logic) provides a discovery-based analysis of on-premise server workloads, collecting performance metrics including CPU utilisation, memory consumption, storage I/O, and network throughput to generate projected cloud cost models and right-sizing recommendations. Cloudamize and Movere offer agent-based and agentless infrastructure discovery platforms that collect detailed performance data from on-premise environments and generate migration readiness assessments and cloud cost models. Microsoft Azure Migrate provides an analogous suite of discovery, assessment, and migration tracking tools for workloads targeted at Microsoft Azure. VMware HCX is specifically designed for the migration of VMware virtualised workloads to VMware-based cloud environments. 

|||||
|---|---|---|---|
|**Tool**|**Strengths**|**Critical Limitations**|**Composite**<br>**Risk Score?**|
|||||
|||||
|AWS Migration<br>Evaluator|<br>Deep<br>AWS<br>cost<br>modelling; right-sizing;<br>RI/SP<br>recommendations|<br>AWS-only;<br>requires<br>agent/data collector; no<br> integrated<br>security<br>assessment|<br> <br>No|
|Cloudamize|Agentless<br>option;<br>multicloud<br>cost<br>comparison; TCO<br>modelling|No<br>integrated<br>cybersecurity<br>assessment; no unified<br>risk score; subscription<br>cost||
||||<br>No|




|||||
|---|---|---|---|
|Azure Migrate|Native<br>Azure<br>integration; dependency<br>visualisation; business<br>case tool|<br> <br> Azure-only;<br>no<br>cybersecurity<br>risk<br>scoring; no composite<br>risk metric|<br>No|
||Broad<br>discovery;<br>application<br>dependency<br>mapping;<br>inventory<br>reports|Agent-based<br>installation required;<br> no<br>security<br>or<br>financial risk scoring|No|
|Movere||||
|||||
|||||
|Manual<br>Risk<br>Register|<br>Widely understood; low<br>cost; flexible|<br>Qualitative only; static;<br>no API integration; no<br>financial modelling|No|
|||||
|This Study's<br>System|Composite 3D score;<br>live AWS pricing; no<br>agent required; PDF<br>audit report|<br> <br>AWS-only pricing; relies<br>on<br>self-reported<br>parameters|<br> <br>YES — 0-<br>100 scale|



**Table 2.5: Comparative Analysis of Existing Cloud Migration Risk** 

## **Assessment Tools** 

## **2.10 Synthesis of Literature Gaps** 

The foregoing review reveals six critical and well-evidenced gaps in the existing body of knowledge and available tooling that collectively justify the design and development of the system proposed in this study. 


1. No existing deployed tool simultaneously quantifies operational, financial, and cybersecurity risks within a single, unified composite risk score for cloud migration projects. Commercial tools either address cost modelling or security assessment, but never both within the same integrated system. 

2. Current commercial tools rely on retrospective analysis of collected infrastructure performance data- requiring agent installation or data collector deployment rather than prospective, parameter-driven risk modelling that enables assessment prior to any data collection, infrastructure access, or organisational commitment. 

3. Neither the academic literature nor any identified commercial tool incorporates realtime cloud pricing API integration into its risk scoring model. Existing financial risk models rely on static pricing tables that rapidly become outdated as cloud providers adjust their pricing, producing inaccurate cost risk assessments. 

4. Existing commercial migration tools do not provide immutable audit trail persistence or automated compliance-grade PDF report generation capabilities that are explicitly required by regulated industries to demonstrate due diligence in risk management documentation. 

5. The academic literature, while producing theoretically sound frameworks for cloud migration risk assessment, has not translated these frameworks into deployable, realworld tools accessible to practising project managers without specialised data science expertise. 

6. No existing system provides a Shared Responsibility Model compliance assessment that explicitly evaluates a proposed migration's security configuration against the customer's cloud security obligations, generating targeted alerts for configuration gaps. 


## **2.11 Chapter Summary** 

This chapter has provided an extensive and critical review of the theoretical and empirical literature underpinning the design of the Cloud Migration Risk Assessment System. The review examined the foundational characteristics and service models of cloud computing; the strategic frameworks for cloud migration and the well-documented operational, financial, and security challenges of enterprise migration projects, the principles of IT risk management and the demonstrated structural limitations of static risk registers, the cloud security governance landscape including the Shared Responsibility Model, IAM risk, encryption requirements, and applicable regulatory compliance frameworks, the financial dynamics of the CapExtoOpEx transition and the FinOps discipline, the serverless computing paradigm, AWS Lambda architecture, and API Gateway integration, the DynamoDB NoSQL database as an audit trail persistence layer, frontend web technologies and Chart.js data visualization, and the capabilities and critical limitations of existing commercial migration assessment tools. The synthesis of these findings confirms the existence of six demonstrable and consequential gaps in existing tools and academic frameworks, and establishes the technical and theoretical foundation upon which the system's architecture, risk scoring algorithm, and validation strategy are built. The following chapter presents the complete research methodology adopted to design, implement, and evaluate this system. 


## **CHAPTER THREE** 

## **RESEARCH METHODOLOGY** 

## **3.0 Introduction** 

This chapter presents the complete scientific and engineering methodology employed to design, develop, and rigorously evaluate the Cloud Migration Risk Assessment System. Every methodological decision documented herein is directly traceable to the research objectives established in Chapter One and the gaps identified in the literature reviewed in Chapter Two. The chapter opens by establishing the research paradigm and philosophical stance underpinning the study, then proceeds through the software development 

methodology, system requirements specification, three-tier serverless architecture design, the complete mathematical specification of the proprietary risk scoring algorithm, the algorithm pseudocode, the system data flow and process flowcharts, the full Python backend source code, the frontend JavaScript implementation, the data collection strategy, the security design, and the multi-level testing and validation strategy. The inclusion of algorithm pseudocode, system flowcharts, and complete program code within this chapter satisfies the academic requirement for full methodological transparency and reproducibility of the developed artefact. 

## **3.1 Research Design** 

## **3.1.1 Research Paradigm: Design Science Research** 

This study is positioned within the Design Science Research (DSR) paradigm- a wellestablished methodology in information systems and software engineering research concerned with the creation and evaluation of innovative artefacts such as constructs, models, algorithms, methods, and implemented systems that solve identified real-world problems and generate new knowledge about how such solutions can be designed and made to work 


(Hevner, March, Park, & Ram, 2004). DSR differs from natural science research, which seeks to describe and explain how the world is, by focusing on the prescriptive creation of artefacts that demonstrate how the world could or should be- it is, in Simon's (1996) terms, the science of the artificial. DSR requires that the artefact be rigorously designed against clearly stated requirements derived from problem analysis, implemented using sound engineering principles, and evaluated against quantitative and qualitative criteria that demonstrate its effectiveness in addressing the identified problem. 

This study follows the six-step DSR process model proposed by Peffers et al. (2007). 

||||
|---|---|---|
|**DSR Step**|**Description**|**Corresponding Study Section**|
||||
|1. Problem<br>Identification &<br>Motivation|Define the specific research problem<br>and justify the value of a solution|<br>Chapter 1, Sections 1.1–1.3|
||||
|2.  Definition<br>of<br>Solution Objectives|<br>Infer the objectives of a solution from<br>the<br>problem<br>definition<br>and<br>knowledge of what is possible|<br> <br>Sections 3.2–3.4 (Requirements)|
||||
||||
|3. Design and<br>Development|Create<br>the<br>artefact:<br>algorithm,<br>architecture,<br>and<br>implemented<br>system|Sections 3.4–3.7 (Architecture &<br>Code)|




||||
|---|---|---|
|4. Demonstration|Demonstrate the use of the artefact to<br>solve one or more instances of the<br>problem|Deployed web application|
||||
|5. Evaluation|Observe and measure how well the<br>artefact supports a solution to the<br>problem|Sections 3.9–3.10 (Testing)|
||||
|6. Communication|Communicate the problem, artefact,<br>utility, and rigour to appropriate<br>audiences|This research report|



**Table 3.1: DSR Process Model Application to This Study (Peffers et al., 2007)** 

## **3.1.2 Mixed-Methods Research Approach** 

This study employs a mixed-methods approach, integrating qualitative and quantitative methods at complementary phases of the research lifecycle. In the qualitative phaseconducted during requirements elicitation, algorithm design calibration, and literature synthesis; a structured thematic analysis was conducted of peer-reviewed academic literature, authoritative industry reports, AWS technical documentation, and regulatory frameworks. This qualitative synthesis was used to derive the taxonomy of migration risk parameters, calibrate scoring thresholds and dimension weights, and populate the mitigation recommendation knowledge base. In the quantitative phase- conducted during system testing and performance validation, twenty-five structured test scenarios were executed against the fully deployed production system, generating numerical risk score outputs evaluated against pre-computed expected values. Apache JMeter performance benchmarking was conducted at 


four concurrent user levels, generating response time distributions evaluated against the three-second performance threshold specified in the nonfunctional requirements. 

## **3.2 Software Development Methodology** 

## **3.2.1 Agile Sprint Structure** 

The Agile software development methodology, underpinned by the values and principles of the Agile Manifesto (Beck et al., 2001), was selected as the primary development framework. Agile was chosen over the sequential Waterfall model because the requirements of a researchled development project are inherently exploratory; the precise configuration of the risk scoring algorithm, the optimal structure of the DynamoDB schema, and the visual design of the interactive dashboard all evolved progressively as insights from the literature review were incorporated. The project is organised into five two-week development sprints totalling a tenweek implementation period. 

||||<br> <br> <br> <br>|
|---|---|---|---|
|**Sprint**|**Duration**|**Primary Deliverables**||
|||||
|||||
|Sprint 1|Weeks 12|<br>Requirements analysis, architecture design, technology stack selection,||
|||||
|||risk parameter taxonomy, API contract definition, Git repository setup,||
|||AWS SAM project initialisation||
|||||
||Weeks 34|Frontend HTML/CSS/JS dashboard, parameter input form with<br>clientside validation, Chart.js radar and doughnut visualisations, Fetch<br>API integration, PDF download handler, responsive layout||
|Sprint 2||||
|||||
|Sprint 3|Weeks 56|<br>Risk Assessment Lambda function (Python 3.11), API Gateway REST||
|||API configuration, Boto3 pricing integration module, three-dimensional||
|||risk scoring algorithm, recommendation engine||
|||||
|||||
|Sprint 4|Weeks 78|DynamoDB table provisioning with GSI, audit trail write/read<br>operations, Report Generation Lambda, ReportLab PDF generation<br>module, base64 response encoding||




||||<br>|
|---|---|---|---|
|Sprint 5|Weeks<br>910|Integration testing, 25-scenario system testing, user acceptance testing||
|||||
|||with||
|||5-member panel, Apache JMeter performance benchmarking at 4||
|||concurrency levels, technical documentation||
|||||



**Table 3.2: Agile Sprint Structure and Deliverables** 

## **3.3 System Requirements Specification** 

## **3.3.1 Functional Requirements** 

|**ID**|**Requirement**|**Priority**|**Verification Method**|
|---|---|---|---|
|||||
|**FR-1**|Web-based<br>parameter<br>input<br>interface<br>accepting structured migration parameters<br>across all three risk dimensions with<br>clientside validation|Must Have|System Test|
|**FR-2**|Computation of composite risk score (0–<br>100) by evaluating parameters across<br>weighted Operational, Financial, and<br>Cybersecurity dimensions|Must Have|Unit & System Test|
|**FR-3**|Risk tier classification: Low (0–39),<br>Medium (40–69), High (70–100),<br>displayed prominently on dashboard with<br>colour-coded badge|<br> <br>Must Have|System Test|
|**FR-4**|Real-time AWS EC2 On-Demand pricing<br>retrieval via Boto3 SDK integrated into<br>Financial Risk sub-score computation|<br>Must Have|Integration Test|




|**FR-5**|Prioritised,<br>actionable<br>mitigation<br>recommendation list tailored to identified<br>vulnerabilities, sorted by severity|<br>Must Have|UAT|
|---|---|---|---|
|**FR-6**|Immutable persistence of all completed<br>assessments in Amazon DynamoDB with<br>write-once IAM enforcement|Must Have|Integration Test|
|**FR-7**|Downloadable PDF compliance report<br>summarising risk scores, identified<br>vulnerabilities, and mitigation<br>recommendations|Must Have|System Test & UAT|
|**FR-8**|Interactive<br>Chart.js<br>radar<br>chart<br>and<br>doughnut gauge updating dynamically with<br>each completed assessment|Should<br>Have|System Test|
|**FR-9**|Real-time retrieval of historical assessments<br>from Amazon DynamoDB.|<br>Should<br>Have|System Test|
|**FR-10**|Generation of downloadable PDF reports<br>using ReportLab.|<br>Should<br>Have|System Test|
|**FR-11**|Interactive radar-chart visualization of<br>Operational, Financial and Security risk<br>dimensions.|Should<br>Have|System Test|



**Table 3.3: Functional Requirements Specification** 

**3.3.2 Non-Functional Requirements** 


|||||
|---|---|---|---|
|**ID**|**Category**|**Requirement**|**Measurement Criterion**|
|||||
|||||
|**NFR-1**|Performance|Risk score computation API|<br>Apache JMeter 95th percentile ≤|
|||||
|||returns response within 3|<br>3000ms|
|||||
|||seconds at p95 under||
|||concurrent load||
|||||
|||||
|**NFR-2**|Scalability|System<br>automatically<br>scales<br>to<br>accommodate<br>concurrent<br>assessment<br>requests without manual<br>intervention|No errors at 50 concurrent users in<br>JMeter test|
|||||
|**NFR-3**|Availability|Target system availability ≥|<br> <br>Architecture<br>relies<br>on<br>AWS|
|||99.9%, consistent with AWS||
|||managed service SLAs|Lambda/API|
|||||
||||GW/DynamoDB SLAs|
|||||
|||||
|**NFR-4**|Security|HTTPS on all endpoints;<br>Principle of Least Privilege<br>IAM<br>roles;<br>DynamoDB<br>encryption at rest; API<br>throttling|<br>Security review and AWS IAM policy<br>audit|
|||||
|**NFR-5**|Usability|Responsive<br>rendering<br>on|<br>UAT checklist; evaluator ratings|
|||desktop<br>browsers;<br>inline|<br>|
|||validation feedback for all||
|||form inputs||
|||||
|||||




|||||||
|---|---|---|---|---|---|
|**NFR-6**|Maintainability|Modular<br>Lambda<br>function<br>architecture;<br>minimum 80% unit test<br>code coverage|pytest-cov coverage report|||
|||||||
|**NFR-7**|Auditability|DynamoDB<br>write-once|<br>IAM<br>policy<br>review;|PITR||
|||||||
|||semantics enforced through|configuration audit|||
|||||||
|||IAM;<br>Point-in-Time||||
|||Recovery enabled||||
|||||||



**Table 3.4: Non-Functional Requirements Specification** 

## **3.4 System Architecture Design** 

## **3.4.1 Three-Tier Serverless Architecture Overview** 

The system adopts a three-tier serverless architecture comprising; A client-side frontend presentation layer built with HTML5, CSS3, and Vanilla JavaScript, A serverless backend compute layer hosted on AWS Lambda and exposed through AWS API Gateway, and A managed data persistence layer implemented using Amazon DynamoDB. This architectural pattern satisfies the scalability, availability, and maintainability requirements without the operational overhead and cost of managing dedicated server infrastructure. All three tiers communicate exclusively through HTTPS-secured RESTful API calls, ensuring a loosely coupled design in which each layer can be independently scaled, modified, and tested without affecting the others. 

## **3.4.2 System Data Flow Diagram** 


The following diagram illustrates the complete end-to-end data flow of the Cloud Migration Risk Assessment System, from the user's input through the API-driven backend to the rendered dashboard and downloadable compliance report. 


**Figure 3.1: System Data Flow Diagram (End-to-End Architecture)** 

## **3.4.3 Risk Assessment Process Flowchart** 

The following flowchart details the internal logic of the Risk Assessment Lambda function, 

illustrating the sequential decision points and computational steps from API request receipt to JSON response dispatch. 



**Figure 3.2: Risk Assessment Lambda- Internal Process Flowchart** 

## **3.5 Risk Scoring Algorithm** 

## **3.5.1 Algorithm Design Principles** 

The risk scoring algorithm is the intellectual core of the system. It accepts the validated migration parameter payload submitted by the user through the frontend form and produces three normalised dimensional sub-scores- Operational (O), Financial (F), and Cybersecurity (Cy) plus a single weighted composite score (C), all expressed on a 0-to100 normalised scale where higher values indicate greater risk exposure. Three design principles guided the algorithm's development; Dimensional Completeness (the algorithm must assess all three principal sources of cloud migration failure simultaneously), Data-driven Calibration (all scoring thresholds, parameter weights, and normalisation function inflection points must be grounded in authoritative empirical evidence from peer-reviewed literature and industry reports), and Interpretability (outputs must be decomposable into their constituent parameter contributions so that users can identify which specific aspects of their migration plan are driving the overall score and what targeted actions can reduce it). 


## **3.5.2 Algorithm Pseudocode** 

The following pseudocode provides a complete, language-independent specification of the risk scoring algorithm, from parameter ingestion through composite score computation to recommendation generation. 

## **ALGORITHM: CloudMigrationRiskScoring  INPUT:** 

## **MigrationParameters P {** 

**data_volume_tb      : Float   // Volume of data to migrate in terabytes     server_count : Integer // Number of servers to migrate     app_complexity      : Enum    // LOW | MEDIUM | HIGH | VERY_HIGH     migration_window_hrs: Integer // Available maintenance window in hours     resource_type       : Enum    //** 

**EC2_SMALL|EC2_MEDIUM|EC2_LARGE|EC2_XLARGE     target_region       :** 

**String  // AWS region code (e.g. eu-west-1)     projected_users     : Integer // Expected concurrent user count     egress_volume_tb    : Float   // Monthly data egress volume in** 

**terabytes     capex_monthly_usd   : Float   // Current on-prem monthly equivalent cost data_sensitivity    : Enum    // PUBLIC|INTERNAL|CONFIDENTIAL|RESTRICTED iam_permissiveness : Enum // LEAST_PRIV|MODERATE|PERMISSIVE|WILDCARD     encryption_posture  :** 

**Enum    // FULL|PARTIAL|TRANSIT_ONLY|NONE     compliance_scope    : Enum //** 

## **NONE|SINGLE|MULTIPLE|CRITICAL** 

**}** 

**OUTPUT: RiskResult R {** 


**assessment_id       : String  // UUID v4     composite_score     : Float   // C in [0, 100] operational_score   : Float   // O in [0, 100]     financial_score     : Float   // F in [0, 100] cybersecurity_score : Float   // Cy in [0, 100]     risk_tier           : String  // LOW | MEDIUM | HIGH     live_price_used     : Boolean** 

**recommendations     : List<Recommendation>[max 10]** 

**}** 

**BEGIN** 

**// ─── PHASE 1: PARAMETER NORMALISATION** 

**──────────────────────────────** 

**// Normalise data_volume_tb → ND using piecewise linear function** 

**IF P.data_volume_tb < 10 THEN** 

**ND ← 10 + (P.data_volume_tb / 10) * 30          // range: 10–40   ELSE IF P.data_volume_tb < 50 THEN** 

**ND ← 40 + ((P.data_volume_tb - 10) / 40) * 35   // range: 40–75   ELSE** 

**ND ← 75 + ((P.data_volume_tb - 50) / 50) * 25   // range: 75–100   END IF ND ← CLAMP(ND, 0, 100)** 

**// Normalise server_count → NS using piecewise linear function** 

**IF P.server_count < 10 THEN** 


**NS ← (P.server_count / 10) * 25                  // range: 0–25   ELSE IF P.server_count** 

**< 50 THEN** 

**NS ← 25 + ((P.server_count - 10) / 40) * 35     // range: 25–60   ELSE IF P.server_count** 

**< 200 THEN** 

**NS ← 60 + ((P.server_count - 50) / 150) * 30    // range: 60–90   ELSE** 

**NS ← MIN(90 + (P.server_count - 200) / 100, 100) // range: 90–100   END IF** 

**// Normalise app_complexity → NA via categorical lookup** 

**NA ← LOOKUP(P.app_complexity, {** 

**LOW: 20, MEDIUM: 45, HIGH: 70, VERY_HIGH: 95   })** 

**// Normalise migration_window_hrs → NW (shorter = higher risk)** 

**IF P.migration_window_hrs >= 72 THEN NW ← 10** 

**ELSE IF P.migration_window_hrs >= 24 THEN** 

**NW ← 10 + ((72 - P.migration_window_hrs) / 48) * 40   // range: 10–50   ELSE IF** 

**P.migration_window_hrs >= 4 THEN** 

**NW ← 50 + ((24 - P.migration_window_hrs) / 20) * 40   // range: 50–90** 

**ELSE** 

**NW ← MIN(90 + (4 - P.migration_window_hrs) * 2.5, 100)   END IF** 

**// ─── PHASE 1B: FINANCIAL  PARAMETER  NORMALISATION** 


**────────────────────** 

**// Fetch live AWS EC2 On-Demand hourly rate via Boto3   TRY WITH TIMEOUT** 

**1500ms:       hourly_rate ← BOTO3_PRICING.get_ec2_price(           region    =** 

**P.target_region,           instance  = MAP(P.resource_type),           os        = 'Linux', tenancy   = 'Shared'** 

**)** 

**live_price_used ← TRUE   CATCH (timeout OR api_error):       hourly_rate ← CACHED_FALLBACK_PRICES[P.resource_type][P.target_region] live_price_used ← FALSE** 

**LOG_TO_CLOUDWATCH('pricing_fallback', P.target_region)   END TRY** 

**monthly_cost_usd ← hourly_rate * 730  // 730 = avg hrs/month** 

**// Normalise projected_monthly_cost → NC** 

**IF monthly_cost_usd < 500 THEN** 

**NC ← (monthly_cost_usd / 500) * 30                     // range: 0–30   ELSE IF** 

**monthly_cost_usd < 5000 THEN** 

**NC ← 30 + ((monthly_cost_usd - 500) / 4500) * 40       // range: 30–70   ELSE** 

**NC ← MIN(70 + ((monthly_cost_usd - 5000) / 5000) * 30, 100)   END IF** 

**// Normalise egress_volume_tb → NE** 


**NE ← CLAMP((P.egress_volume_tb / 10) * 80 + 10, 10, 100)** 

**// Normalise capex_to_opex_delta → NT** 

**delta ← ABS(monthly_cost_usd - P.capex_monthly_usd) /** 

**MAX(P.capex_monthly_usd, 1)** 

**NT ← CLAMP(delta * 100, 0, 100)** 

**// ─── PHASE 1C: CYBERSECURITY PARAMETER NORMALISATION** 

**────────────────** 

**NSens ← LOOKUP(P.data_sensitivity, {** 

**PUBLIC: 10, INTERNAL: 30, CONFIDENTIAL: 65, RESTRICTED: 95   })** 

**NIAM ← LOOKUP(P.iam_permissiveness, {** 

**LEAST_PRIV: 10, MODERATE: 35, PERMISSIVE: 70, WILDCARD: 98   })** 

**NEnc ← LOOKUP(P.encryption_posture, {** 

**FULL: 5, PARTIAL: 35, TRANSIT_ONLY: 65, NONE: 95   })** 

**NComp ← LOOKUP(P.compliance_scope, {** 

**NONE: 5, SINGLE: 30, MULTIPLE: 60, CRITICAL: 90   })** 


**// ─── PHASE 2: DIMENSIONAL SUB-SCORE COMPUTATION** 

**─────────────────────** 

**O  ← (0.30 * ND) + (0.25 * NS) + (0.30 * NA) + (0.15 * NW) F  ← (0.45 * NC) + (0.30 * NE) + (0.25 * NT)** 

**Cy ← (0.35 * NSens) + (0.30 * NIAM) + (0.20 * NEnc) + (0.15 * NComp)** 

**O  ← ROUND(O,  2)** 

**F  ← ROUND(F,  2)** 

**Cy ← ROUND(Cy, 2)** 

**// ─── PHASE 3: COMPOSITE SCORE ────────────────────────────────────────** 

**C ← (0.35 * O) + (0.30 * F) + (0.35 * Cy) C ← ROUND(C, 2)** 

**// ─── PHASE 4: RISK TIER CLASSIFICATION ──────────────────────────────** 

**IF C < 40 THEN      tier ← 'LOW'** 


**ELSE IF C < 70 THEN tier ← 'MEDIUM'** 

**ELSE                tier ← 'HIGH'** 

**END IF** 

**// ─── PHASE 5: RECOMMENDATION ENGINE ─────────────────────────────────** 

## **recommendations ← EMPTY_LIST** 

**parameter_contributions ← {** 

**'Data Volume'       : {score: ND,    dim: 'Operational',    thresh: 60},** 

**'Server Count'      : {score: NS,    dim: 'Operational',    thresh: 60},** 

**'App Complexity'    : {score: NA,    dim: 'Operational',    thresh: 60},** 

**'Migration Window'  : {score: NW,    dim: 'Operational',    thresh: 60}, 'Monthly Cost'      : {score: NC,    dim: 'Financial',      thresh: 55}, 'Data Egress'       : {score: NE,    dim: 'Financial',      thresh: 55}, 'CapEx-OpEx Delta'  : {score: NT,    dim: 'Financial',      thresh: 55},** 

**'Data Sensitivity'  : {score: NSens, dim: 'Cybersecurity',  thresh: 50},** 

**'IAM Permissiveness': {score: NIAM,  dim: 'Cybersecurity',  thresh: 50}, 'Encryption'        : {score: NEnc,  dim: 'Cybersecurity',  thresh: 50}, 'Compliance Scope'  : {score: NComp, dim: 'Cybersecurity',  thresh: 50}   }** 


**FOR EACH (param_name, param_data) IN parameter_contributions:       IF param_data.score > param_data.thresh THEN** 

**rec ← LOOKUP_RECOMMENDATION(param_name, param_data.score)** 

**IF param_data.score >= 80 THEN rec.priority ← 'CRITICAL'** 

**ELSE IF param_data.score >= 60 THEN rec.priority ← 'IMPORTANT'** 

**ELSE rec.priority ← 'ADVISORY'** 

**END IF** 

**APPEND rec TO recommendations** 

**END IF** 

**END FOR** 

**SORT  recommendations BY (priority DESC, param_data.score DESC)   recommendations ← TAKE_FIRST(recommendations, 10)** 

**// ─── PHASE 6: AUDIT TRAIL PERSISTENCE** 

**───────────────────────────────** 

**assessment_id ← GENERATE_UUID_V4()** 

**timestamp     ← CURRENT_UTC_DATETIME_ISO8601()** 

**DYNAMODB.put_item({** 


**AssessmentId    : assessment_id,** 

**Timestamp       : timestamp,** 

**CompositeScore  : C,** 

**OperationalScore: O,** 

**FinancialScore  : F,** 

**CybersecScore   : Cy,** 

**RiskTier        : tier,** 

**InputParameters : P,** 

**Recommendations : recommendations,** 

**LivePriceUsed   : live_price_used,** 

**MonthlyEstUSD   : monthly_cost_usd** 

**}, ConditionExpression: 'attribute_not_exists(AssessmentId)')** 

**// ─── PHASE 7: CONSTRUCT AND RETURN RESPONSE** 

**─────────────────────────** 

**RETURN HTTP_200 {       assessmentId      : assessment_id,       compositeScore    : C, operationalScore  : O,       financialScore    : F,       cybersecurityScore: Cy,       riskTier : tier,       recommendations   : recommendations,       livePrice         : live_price_used, monthlyEstUSD     : monthly_cost_usd   }** 

**END ALGORITHM** 


## **3.5.3 Mathematical Specification of Sub-Scores** 

The three-dimensional sub-scores and composite score are expressed formally as follows: 

Operational Sub-Score: 

**O = (0.30 × N_D) + (0.25 × N_S) + (0.30 × N_A) + (0.15 × N_W)** 

Financial Sub-Score: 

**F = (0.45 × N_C) + (0.30 × N_E) + (0.25 × N_T)** 

**Cybersecurity Sub-Score:** 

**Cy = (0.35 × N_Sens) + (0.30 × N_IAM) + (0.20 × N_Enc) + (0.15 × N_Comp)** 

Composite Risk Score: 

**C = (0.35 × O) + (0.30 × F) + (0.35 × Cy)** 

Where all parameters N_x  [0, 100] and all weights sum to 1.00 per dimension. 

Weight justification: 

Operational (0.35): Downtime during cutover can be catastrophic and irreversible 

Financial   (0.30): Overruns are serious but typically remediable via budget action 

Cybersecurity(0.35): Breaches produce irrecoverable reputational / regulatory harm 

**Figure 3.4: Mathematical Specification of the Three-Dimensional Risk Scoring Model** 


||||||<br> <br> <br> <br>|
|---|---|---|---|---|---|
|**Parameter**|**Symbol**|**Dimension**|**Weight**|**Normalisation Method**||
|||||||
|Data Volume (TB)|N_D|Operational|0.30|Piecewise linear: 3 segments at 10TB,<br>50TB inflection points||
|||||||
|Server Count|N_S|Operational|0.25|Piecewise linear: 4 segments at 10,<br>50,<br>200 inflection points||
|||||||
|App<br>Dependency<br>Complexity|<br>N_A|Operational|0.30|Categorical lookup: LOW=20,<br>MEDIUM=45, HIGH=70,<br>VERY_HIGH=95||
|||||||
|Migration Window<br>(hrs)|N_W|Operational|0.15|Inverse piecewise: shorter window →<br>higher risk score||
|||||||
|Projected Monthly<br>Cost (USD)|N_C|Financial|0.45|Piecewise linear using live Boto3<br>AWS pricing; 3 segments||
|||||||
|Data Egress Volume<br>(TB/mo)|<br>N_E|Financial|0.30|Linear: NE = clamp((V/10) ×80 + 10,<br>10, 100)||
|||||||
|CapEx-OpEx<br>Transition Delta|N_T|Financial|0.25|Relative cost delta: |cloud_cost -<br>on_prem_cost| / on_prem_cost × 100||
|||||||
|Data Sensitivity|N_Sens|Cybersecurity|0.35|Categorical lookup: PUBLIC=10,<br>INTERNAL=30,<br>CONFIDENTIAL=65,<br>RESTRICTED=95||




||||||<br>|
|---|---|---|---|---|---|
|IAM<br>Permissiveness|N_IAM|<br>Cybersecurity|<br>0.30|Categorical<br>lookup:<br>LEAST_PRIV=10,<br>MODERATE=35, PERMISSIVE=70,||
|||||||
|||||WILDCARD=98||
|||||||
|Encryption Posture|N_Enc|Cybersecurity|0.20|Categorical lookup: FULL=5,<br>PARTIAL=35,<br>TRANSIT_ONLY=65,<br>NONE=95||
|||||||
|Compliance<br>Framework Scope|N_Comp|<br>Cybersecurity|<br>0.15|Categorical lookup: NONE=5,<br>SINGLE=30, MULTIPLE=60,<br>CRITICAL=90||



**Table 3.5: Complete Risk Parameter Specification with Symbols, Weights, and** 

## **Normalisation Methods** 

The weighting structure adopted in the risk scoring model was derived from a synthesis of industry reports, cloud migration case studies, and cloud security governance literature. Operational Risk was assigned a weight of 35% because migration failure is frequently associated with application complexity, dependency mapping errors, and data transfer challenges. Cybersecurity Risk was also assigned 35% due to the prevalence of cloud misconfiguration incidents, access control failures, and regulatory penalties. Financial Risk was assigned 30% because although financial overruns are significant, they are generally easier to detect and correct than security or operational failures. The weighting model was subjected to sensitivity analysis using multiple simulated migration scenarios to ensure that no single parameter disproportionately influenced the composite score. 


## **3.6 Technology Stack Justification** 

|||||
|---|---|---|---|
|**Component**|**Technology**<br>**Selected**|**Version**|**Justification**|
|||||
|Frontend|HTML5, CSS3,<br>Vanilla JavaScript|ES2022|No framework overhead, full native API<br>access, broad browser compatibility<br>without transpilation|
|||||
|Data<br>Visualisation|Chart.js|v4.x|Canvas-based rendering, radar and<br>doughnut chart types, responsive;<br>zero backend dependency|
|||||
|Backend<br>Runtime|Python|3.11|Rich ecosystem; Boto3 native support;<br>low cold-start latency (~200ms);<br>comprehensive testing libraries|
|||||
|Compute Layer|AWS Lambda|Python 3.11<br>runtime|Serverless, automatic scaling, zero idle<br>cost, eliminates server management<br>operational risk|
|||||
|API Layer|AWS API Gateway|REST API|Managed HTTPS, CORS, throttling,<br>Lambda proxy integration, built-in<br>DDoS protection|
|||||
|Cloud SDK|Boto3 (AWS SDK<br>for Python)|1.34+|Official AWS SDK; required for Pricing<br>API and DynamoDB<br>integration, actively maintained|




|||||
|---|---|---|---|
|Database|Amazon<br>DynamoDB|On-demand<br>capacity|Serverless,<br>schema-flexible,<br>singledigit<br>ms<br>latency,<br>PITR,<br>immutable write semantics via IAM|
|||||
|PDF Generation|ReportLab|v4.x|Production-grade PDF library, runs in<br>Lambda, supports tables, colours,<br>styles, page layout|
|||||
|IaC<br>Deployment|AWS SAM<br>(Serverless App<br>Model)|Latest CLI|Lambda-native IaC, local testing with<br>SAM Local, YAML template, single<br>deployment command|
|||||
|Unit Testing|pytest + pytest-cov|8.x|Standard Python test framework, rich<br>assertion library, coverage measurement<br>with line-level<br>reporting|
|||||
|Performance<br>Testing|Apache JMeter|5.6|Industry<br>standard,<br>concurrent<br>load<br>simulation, p95 latency measurement;<br>CSV result export|



**Table 3.6: Technology Stack Selection and Justification** 

## **3.7 Security Design** 

Security is treated as a first-class architectural concern throughout the system, embodying the 

shift-left security philosophy that the system itself advocates to its users. Seven security controls are implemented across all layers of the system architecture. 


||||
|---|---|---|
|**Security Control**|**Implementation**|**Threat Mitigated**|
||||
|Transport Encryption|TLS 1.2+ enforced on all API<br>Gateway endpoints, HTTPS-only<br>URLs|Man-in-the-middle<br>attacks, data interception<br>in transit|
||||
|**Security Control**|**Implementation**|**Threat Mitigated**|
||||
|Principle of Least Privilege|Risk Assessment Lambda:<br>dynamodb:PutItem<br>+<br>pricing:GetProducts only. Report<br>Lambda:<br>dynamodb:GetItem<br>+<br>dynamodb:Query<br>only.<br>Neither<br>granted UpdateItem, DeleteItem, or<br>administrative permissions.|Privilege<br>escalation,<br>lateral movement, data<br>tampering|
||||
||||
|Data Encryption at Rest|DynamoDB  SSE  using  AWS-<br>managed KMS keys (AES-256)|Unauthorised physical or<br>logical storage access|
||Two independent validation layers:<br>client-side JavaScript (UX) and<br> serverside<br>Lambda<br>schema<br>validation<br>(security control)|<br>Injection<br>attacks,<br>malformed payloads,<br>business logic bypass|
|Input Validation<br>(Defence-in-Depth)|||
||||




||||
|---|---|---|
||||
|API Throttling|100 requests/second steady-state;<br> 200request  burst  limit<br>at API<br>Gateway level|Denial-of-service attacks,<br>Lambda<br>concurrency<br>exhaustion, cost runaway|
|Immutable Audit Trail|DynamoDB<br>write-once<br>semantics enforced through<br>IAM<br>restrictions,<br>ConditionExpression<br>prevents<br>overwriting existing records|<br>Audit<br>trail<br>tampering,<br>compliance<br>documentation integrity|
||||
|Operational Logging|All Lambda invocations, pricing<br>fallbacks, and errors logged to AWS<br>CloudWatch with structured JSON<br>format|Incident detection;<br>forensic investigation,<br>operational<br>monitoring|



**Table 3.7: Security Controls Implementation Matrix** 

## **3.8 Testing and Validation Strategy** 

## **3.8.1 Unit Testing** 

Unit tests were authored for each discrete Python function within the Lambda modules using the pytest framework, with all external dependencies replaced by controlled mock objects through Python's unittest.mock library. This isolation ensures deterministic, repeatable tests that neither incur live AWS API costs nor depend on network availability. Three categories of test cases were implemented for each function: nominal cases testing expected behaviour with typical parameter values; boundary cases testing the exact inflection points of the piecewise normalisation functions (D = 10 TB, D = 50 TB, S = 10, S = 50, S = 200, W = 4 hrs, W = 24 hrs, W = 72 hrs); and edge cases testing minimum and maximum valid parameter 


values. A minimum code coverage target of 80% was required for all Lambda modules, measured using pytest-cov with line-level reporting. 

## **3.8.2 Integration Testing** 

Integration tests validated the complete end-to-end request flow from frontend form submission through API Gateway to Lambda execution and DynamoDB write, executed against a dedicated development environment provisioned using AWS SAM Local. 

DynamoDB Local- Amazon's locally executable replica of the DynamoDB service, was used to simulate the database persistence layer, seeded with pre-existing records to test retrieval logic and GSI query performance. Integration tests verified; JSON payload serialisation and deserialisation correctness across the frontend-to-API-Gateway boundary; algorithm score correctness for submitted parameter sets against pre-computed expected values; DynamoDB record attribute structure and field type correctness; and correct Chart.js visualisation rendering in response to API responses injected into the frontend via mock fetch responses. 

## **3.8.3 System Testing- 25-Scenario Test Matrix** 

System testing executed twenty-five pre-designed structured scenarios against the fully deployed production system. The scenarios were constructed using a stratified design: eight scenarios targeted Low Risk outcomes (0-39), ten targeted Medium Risk (40-69), and seven targeted High Risk (70-100). Five additional scenarios tested boundary and edge conditions. For each scenario, the expected composite score was manually pre-computed using the algorithm's published formulas before system execution, providing a ground truth for validation. A tolerance of ±0.5 was applied for floating-point arithmetic. 


||||||
|---|---|---|---|---|
|**Scenario Category**|**Count**|**Risk**<br>**Target**<br>**Tier**||**Design Focus**|
||||||
||||||
|Low Risk (Standard)|5|0–39||Well-planned, small-scale migrations|
|||||with strong security posture|
||||||
||||||
|Low Risk (Edge)|3|0–39||Minimum parameter values testing<br>lower bounds of all normalisation<br>functions|
||||||
|Medium Risk (Security|4|40–69||Elevated cybersecurity scores with|
|||||moderate operational and financial risk|
|Dominant)|||||
||||||
||||||
|Medium Risk (Financial-<br>Dominant)|3|40–69||High projected cost and egress volume;<br>controlled security posture|
||||||
|Medium<br>Risk|<br>3|40–69||Large data volumes and server counts;|
|||||strong security configuration|
|(Operational-Dominant)|||||
||||||
||||||
|High<br>Risk<br>(All<br>Dimensions)|<br>3|70–100||Simultaneously elevated scores across<br>all three dimensions|
||||||
|High Risk (Cybersecurity-|2|70–100||Wildcard IAM, no encryption, restricted|
|||||data, critical compliance scope|
|Led)|||||
||||||
||||||
|High Risk (Scale-Led)|2|70–100||Very large infrastructure scale; tight<br>migration window|
||||||




||||||
|---|---|---|---|---|
||||||
|Boundary Conditions|5|Mixed||Parameters at exact inflection points|
||||||
||||||
|||||(D=10, D=50, S=50, W=24, W=4)|
||||||



## **Table 3.8: System Test Scenario Stratified Design Matrix 3.8.4 User Acceptance Testing** 

User acceptance testing was conducted with five evaluators drawn from three professional backgrounds: two IT project management professionals with direct cloud migration experience; two final-year computer science postgraduate students with cloud computing specialisations; and one IT auditor with compliance documentation and regulatory reporting experience. Each UAT session comprised three phases: An introductory briefing explaining the system's purpose and the session structure, without disclosing the scoring algorithm to avoid bias in usability judgments, a think-aloud task execution phase during which each evaluator completed three predefined assessment scenarios and verbalised their observations, and a structured evaluation using a twelve-item questionnaire covering functional completeness, interface clarity, dashboard comprehensibility, recommendation relevance, PDF report quality, and perceived utility relative to manual risk register methods. Sessions were conducted remotely with screen recording and verbal commentary captured for analysis. 

A structured evaluation instrument based on a five-point Likert scale was used to collect user feedback. Evaluation criteria included ease of navigation, clarity of visualisations, usefulness of recommendations, perceived accuracy of risk scores, and overall satisfaction. Results were analysed using descriptive statistics and narrative observations. 

## **3.8.5 Performance Benchmarking** 

Apache JMeter 5.6 was used to benchmark the end-to-end latency of the POST /assess endpoint under simulated concurrent load at four concurrency levels; 1, 10, 25, and 50 virtual users. Each test scenario ran for 60 seconds after a 10-second linear ramp-up period, with each virtual user submitting a standardised assessment payload (a pre-defined Medium Risk 


scenario) in a continuous loop without think time. For each concurrency level, four primary metrics were recorded; average response time (ms), 95th percentile response time (ms), minimum response time (ms), and HTTP error rate (%). The performance acceptance criterion was that the 95th percentile response time must not exceed 3,000ms (NFR-1) and the HTTP error rate must not exceed 1% at any tested concurrency level. 

## **3.9 Ethical Considerations** 

This study was conducted in full compliance with the institution's research ethics guidelines and does not involve the collection or processing of personally identifiable information from human subjects in a manner that would require formal ethics committee approval beyond standard project management oversight. All twenty-five system test scenarios were synthetically constructed by the researcher and do not represent real organisational infrastructure, real financial data, or the data assets of any identifiable enterprise. UAT participants provided signed informed consent before engaging in sessions, were fully briefed on the academic nature of the study, were informed of their unconditional right to withdraw at any time without consequence, and no personal information beyond professional background category was collected or stored. Participant feedback data was recorded only in anonymised, aggregated form. All third-party software libraries are used in compliance with their respective open-source licences (Apache 2.0 for Boto3, MIT for Chart.js, BSD for ReportLab, MIT for pytest). The system's PDF report and frontend dashboard include prominent disclaimer text advising users that assessment outputs are decision-support tools requiring professional judgment, not authoritative determinations. 

## **3.10 Chapter Summary** 

This chapter has presented the complete methodological framework for the design, development, and validation of the Cloud Migration Risk Assessment System. The study was 


positioned within the Design Science Research paradigm with a pragmatist philosophical stance and a mixed-methods research approach. An Agile sprint methodology structured the ten-week implementation across five focused two-week sprints with clear, measurable deliverables at each stage. Eight functional and seven non-functional requirements were systematically derived from the research objectives and the literature gaps identified in Chapter Two. The three-tier serverless architecture was specified in full, encompassing the frontend single-page application, the dual Lambda function backend, the API Gateway configuration, and the DynamoDB table design. The system data flow diagram (Figure 3.1) and the Risk Assessment Lambda process flowchart (Figure 3.2) provide complete visual representations of system behaviour. The proprietary risk scoring algorithm was documented in full through pseudocode (Algorithm 3.1), mathematical specification (Figure 3.3), and parameter weight tables (Table 3.5). Complete, deployable Python source code for both Lambda functions (Code Listings 3.1 and 3.2) and the frontend JavaScript application (Code Listing 3.3) was presented, providing full methodological transparency. The security design and multi-level testing strategy- spanning unit, integration, system, user acceptance, and performance testing — were specified in detail. The following chapter presents the implementation details, testing results, and evaluation findings. 

**References** 

**Academic & Research Literature** 


- **Bannerman, P. L.** (2008). Risk and risk management in software projects: A reassessment. _Journal of Systems and Software_ , _81_ (12), 2118–2133. 

- **Hevner, A. R., March, S. T., Park, J., & Ram, S.** (2004). Design science in information systems research. _MIS Quarterly_ , _28_ (1), 75–105. 

- **Jamshidi, P., Ahmad, A., & Pahl, C.** (2013). Cloud migration research: A systematic review. _IEEE Transactions on Cloud Computing_ , _1_ (2), 142–157. 

- **Kutsch, E., & Hall, M.** (2010). Deliberate ignorance in project risk management. _International Journal of Project Management_ , _28_ (3), 245–255. 

- **Leitner, P., Wittern, E., Spillner, J., & Hummer, W.** (2019). A source-level empirical study of the cold start problem in serverless computing. _IEEE Transactions on Cloud Computing_ , _7_ (4), 1024–1037. 

- **McCrory, D.** (2010). _Data gravity - Definition_ . McCrory Digital. 

- **Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S.** (2007). A design science research methodology for information systems research. _Journal of Management Information Systems_ , _24_ (3), 45–77. 

- **Simon, H. A.** (1996). _The sciences of the artificial_ (3rd ed.). MIT Press. 

**Industry, Government & Technical Reports** 

• **Amazon Web Services.** (2023). _AWS security documentation: The Shared Responsibility Model_ . https://aws.amazon.com/compliance/shared- 

responsibilitymodel/ 

- **Amazon  Web  Services.** (2023). _AWS  Lambda developer guide_ . 

https://docs.aws.amazon.com/lambda/ 

- **Bhardwaj, S., Jain, L., & Jain, S.** (2010). Cloud computing: A study of 

infrastructure as a service (IaaS). _International Journal of Engineering and_ 


_Information Technology_ , _2_ (1), 60–63. 

- **Buyya, R., Pandey, S., & Vecchiola, C.** (2009). Cloud computing and emerging IT 

platforms: Vision, hype, and reality for delivering computing as the 5th utility. _Future_ 

_Generation Computer Systems_ , _25_ (6), 599–616. 

- **Cloud Security Alliance.** (2022). _Top threats to cloud computing: Egregious eleven_ 

https://cloudsecurityalliance.org/artifacts/top-threats-to-cloud-computing- 

egregiouseleven/ 

- **FinOps  Foundation.** (2023). _FinOps framework_ . 

https://www.finops.org/framework/ 

• **Flexera.** (2023). _Flexera 2023  state  of the cloud  report_ . 

https://www.flexera.com/blog/cloud/cloud-computing-trends-2023-state-of- 

thecloud-report/ 

- **Gartner.** (2019). _Guidance for cloud migration strategies_ . Gartner Research Note. 

- **International Data Corporation.** (2019). _Enterprise cloud migration outcomes and_ 

_impact study_ . IDC Whitepaper. 

- **International Organization for Standardization.** (2018). _Risk management —_ 

_Guidelines_ (ISO Standard No. 31000:2018). 

https://www.iso.org/standard/65694.html 

- **Mell, P., & Grance, T.** (2011). _The NIST definition of cloud computing_ (Special 

Publication 800-145). National Institute of Standards and Technology. 

https://csrc.nist.gov/publications/detail/sp/800-145/final 

- **National Institute of Standards and Technology.** (2012). _Guide for conducting risk_ 

_assessments_ (Special Publication 800-30 Revision 1). U.S. Department of Commerce. https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final 

- **Ponemon Institute.** (2022). _Cost of a data breach report 2022_ . IBM Security. 

https://www.ibm.com/reports/data-breach 


## **Regulatory Frameworks & Standards (Contextual Citations)** 

- **COBIT 5:** _COBIT 5: A business framework for the governance and management of enterprise IT_ . (2012). ISACA. 

- **FAIR Model:** _Standard for factor analysis of information risk (FAIR)_ . (2020). The Open Group Standard. 

- **GDPR Article 32:** Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data (General Data Protection Regulation). _Official Journal of the European Union_ , L119, 1–88. 

- **HIPAA Security Rule:** Health Insurance Portability and Accountability Act of 1996, Public Law 104-191, 110 Stat. 1936. 

- **ISO/IEC 27001:** _Information technology — Security techniques — Information security management systems — Requirements_ (ISO/IEC Standard No. 27001:2022). (2022). International Organization for Standardization. 

- **NIST CSF:** _Framework for improving critical infrastructure cybersecurity, Version 1.1_ . (2018). National Institute of Standards and Technology. 

- **PCI DSS v4.0:** _Payment card industry data security standard: Requirements and security assessment procedures version 4.0_ . (2022). PCI Security Standards Council. 

- **PMBOK Guide:** Project Management Institute. (2021). _A guide to the project management body of knowledge (PMBOK guide)_ (7th ed.). 

- **Sarbanes-Oxley Act:** Sarbanes-Oxley Act of 2002, Pub. L. No. 107-204, 116 Stat. 745 (2002). 



## **CHAPTER FOUR**

## **DESIGN AND IMPLEMENTATION**

## **4.0 Introduction**

This chapter presents the implementation, testing, and validation results of the developed Cloud Migration Risk Assessment System (CloudRA). It describes the software architecture, the specific programming details, the user interface design, and the validation strategy used to verify that the system satisfies both functional and non-functional requirements. The chapter also details the test coverage results, showing how the piecewise normalisation algorithms and database persistence layers perform under automated verification scenarios.

## **4.1 System Implementation Overview**

The implementation of the CloudRA system realises the academic models established in previous chapters through a modern, hybrid-architecture web application. The system is designed to provide dual-mode persistence, being deployable natively on Amazon Web Services for production-grade cloud operations or run completely locally using embedded SQLite storage for offline presentations and academic demonstrations. The architecture is optimised for zero-latency, presentation-grade operations, ensuring that all features function reliably regardless of network availability or AWS credential configuration.

The system architecture follows a three-tier design comprising a frontend presentation layer, a backend API services layer, and a persistence and cloud integration layer. The frontend presentation layer is built using semantic HTML5, CSS3 Custom Properties implementing the Stillwater Design System, and object-oriented Vanilla JavaScript conforming to the ES2022 specification. The frontend communicates asynchronously with the backend via HTTPS JSON payloads using the browser's native Fetch API. In static serverless configurations, such as the GitHub Pages deployment used for public demonstration, the JavaScript controller automatically toggles into a Presentation Sandbox Mode that executes the entire scoring algorithm and state management engine client-side using the browser's localStorage API, eliminating any dependency on the Python backend.

The backend API services layer is implemented using the Python 3.12 Flask micro-framework, providing secure session-based authentication guards, assessment CRUD (Create, Read, Update, Delete) operations, and automated PDF compliance report generation via the ReportLab library. The Flask application exposes RESTful JSON endpoints for assessment submission, retrieval, listing, and deletion, as well as HTML-serving routes for the landing page, login portal, and authenticated dashboard.

The AWS SDK integration layer is powered by the official AWS SDK for Python, Boto3 (version 1.34+), executing connections to two AWS services. The first is the AWS Pricing Service API, which queries real-time on-demand pricing rates for EC2 instance configurations within the standard us-east-1 pricing catalog endpoint. The second is the AWS DynamoDB Service, which provides managed NoSQL table provisioning, item writing, scanning, and deletion operations for persistent cloud-hosted storage of assessment records.

The hybrid persistence adapter uses a polymorphic design pattern to switch between storage backends at runtime. If the environment variable USE_DYNAMODB is set to true and valid AWS credentials are available, all assessment records are written directly to the remote AWS DynamoDB table named CloudRiskAssessments. If the flag is absent, or if AWS credentials or internet connectivity are unavailable, the adapter falls back gracefully to a local SQLite database file (assessments.db) whose table schema and column names are designed to mirror the DynamoDB attribute structure exactly, ensuring data portability between the two backends.

To ensure zero network latency during academic reviews and offline presentations, the application implements several presentation performance features. Google Fonts Fraunces and Inter are bundled locally as compressed WOFF2 (Web Open Font Format 2) files and linked through local @font-face CSS bindings, eliminating dependency on external font CDN servers. Grid backdrops and linen grain texturing are encoded directly into the local stylesheets as base64-encoded SVG data URIs, removing the need for external image requests. The AWS Pricing API call is wrapped in a strict 1.5-second timeout; if the call exceeds this threshold or encounters a network error, the system immediately falls back to a hardcoded local pricing table containing cached EC2 on-demand rates for four AWS regions, ensuring that financial risk calculations always return valid results.

## **4.2 Design Components (The Logic)**

The core logic of the CloudRA scoring engine implements the mathematical formulations and categorical scoring lookups established in Chapters 2 and 3. The assessment converts fourteen distinct input parameters into three dimensional sub-scores (Operational, Financial, and Cybersecurity), which are then combined into a single composite risk index using a weighted linear combination.

## _**4.2.1 Operational Dimension Scoring**_

Operational risk measures the physical and structural complexity of the workload migration. Four parameters contribute to the operational sub-score, each normalised to a value between 0.0 and 1.0 before weighting.

Data Volume (N_data) is normalised using a three-segment piecewise linear function applied to the input volume in terabytes. For volumes between 0 and 10 TB, the normalised score ranges linearly from 0.0 to 0.4, reflecting low operational complexity for small-scale data migrations. For volumes between 10 and 100 TB, the score ranges from 0.4 to 0.8, representing moderate complexity. For volumes between 100 and 1,000 TB, the score ranges from 0.8 to 1.0, representing high-complexity enterprise-scale migrations where data gravity effects become significant.

Server Count (N_servers) is normalised using a three-segment piecewise linear function applied to the total number of servers to be migrated. For counts between 0 and 50, the normalised score ranges from 0.0 to 0.5. For counts between 50 and 200, the score ranges from 0.5 to 0.85. For counts between 200 and 2,000, the score ranges from 0.85 to 1.0, reflecting the diminishing marginal increase in operational complexity as infrastructure scales to very large deployments.

Application Complexity (N_complexity) is determined by a categorical lookup function based on the system architecture classification selected by the user. The lookup values are: LOW = 0.1 (static web pages and standalone servers), MEDIUM = 0.4 (standard N-tier applications with localised databases), HIGH = 0.8 (distributed microservices with transactional databases), and VERY_HIGH = 1.0 (legacy monolithic applications with mainframe integrations).

Migration Cutover Window (N_window) is normalised using a three-segment piecewise linear function applied to the acceptable maintenance window in hours. This parameter uses an inverse relationship, meaning that shorter windows produce higher risk scores. For windows between 0 and 12 hours, the normalised score ranges from 1.0 down to 0.8, reflecting the high risk associated with extremely tight cutover deadlines. For windows between 12 and 48 hours, the score ranges from 0.8 down to 0.3. For windows between 48 and 168 hours (one week), the score ranges from 0.3 down to 0.0, reflecting the reduced operational risk afforded by generous migration timelines.

The operational risk sub-score is then derived using a weighted linear combination of the four normalised parameters: Operational = (0.30 * N_data + 0.25 * N_servers + 0.30 * N_complexity + 0.15 * N_window) * 100. This produces a score on a 0-to-100 scale, where higher values indicate greater operational migration risk.

## _**4.2.2 Financial Dimension Scoring**_

Financial risk models budgetary exposure and monthly infrastructure run costs against the organisation's existing on-premises capital expenditure baseline. Three parameters contribute to the financial sub-score.

Monthly Cost Run (N_cost) is normalised using a three-segment piecewise linear function applied to the estimated monthly AWS infrastructure cost in US dollars. This cost is computed by multiplying the live (or cached) EC2 on-demand hourly rate for the selected instance type and region by the server count and by 730 hours per month. For monthly costs between $0 and $2,000, the normalised score ranges from 0.0 to 0.4. For costs between $2,000 and $10,000, the score ranges from 0.4 to 0.85. For costs between $10,000 and $100,000, the score ranges from 0.85 to 1.0.

Network Egress Volume (N_egress) is normalised linearly. The input egress volume in terabytes is divided by 50, with a maximum cap of 1.0. This reflects the significant data transfer charges that AWS applies to outbound traffic, which are frequently underestimated in migration planning.

Cost Delta (N_delta) measures the budget differential between the projected AWS monthly cost (C_aws) and the organisation's current on-premises monthly CapEx (C_prem). The delta is defined as C_aws minus C_prem. For negative deltas (where cloud costs are lower than on-premises costs) ranging from negative $10,000 to $0, the normalised score ranges from 0.0 to 0.3, reflecting minimal financial risk. For positive deltas (where cloud costs exceed on-premises costs) ranging from $0 to $20,000, the score ranges from 0.3 to 1.0, reflecting increasing financial exposure.

The financial risk sub-score is defined as: Financial = (0.45 * N_cost + 0.30 * N_egress + 0.25 * N_delta) * 100.

## _**4.2.3 Cybersecurity Dimension Scoring**_

Cybersecurity risk measures the security surface exposure and configuration posture of the proposed cloud deployment. Four categorical parameters contribute to the cybersecurity sub-score, each assigned a fixed normalised value based on the classification selected by the user.

Data Sensitivity Class (N_sens) assigns risk scores based on the data classification level: PUBLIC = 0.0 (publicly available data with no confidentiality requirements), INTERNAL = 0.3 (internal corporate data not intended for public disclosure), CONFIDENTIAL = 0.7 (sensitive business or customer data subject to access controls), and RESTRICTED = 1.0 (highly regulated data subject to statutory protection requirements such as GDPR, HIPAA, or PCI DSS).

IAM Posture Permissiveness (N_iam) assigns risk scores based on the access control configuration scope: LEAST_PRIV = 0.0 (strict principle of least privilege with scoped role-based access), MODERATE = 0.3 (standard role-based access with limited administrative scope), PERMISSIVE = 0.7 (broad access grants with insufficient boundary controls), and WILDCARD = 1.0 (unrestricted wildcard IAM policies granting full administrative access to all resources).

Encryption Coverage (N_enc) assigns risk scores based on the encryption posture: FULL = 0.0 (comprehensive encryption covering both data in transit via TLS and data at rest via KMS), PARTIAL = 0.4 (encryption at rest only, with transit data unprotected), TRANSIT_ONLY = 0.7 (transit encryption only, with stored data unencrypted), and NONE = 1.0 (no encryption, with all data stored and transmitted in plaintext).

Compliance Governance Scope (N_comp) assigns risk scores based on the number and criticality of external regulatory frameworks applicable to the migration: NONE = 0.0 (no external compliance obligations), SINGLE = 0.3 (subject to one regulatory framework), MULTIPLE = 0.7 (subject to multiple overlapping regulatory frameworks), and CRITICAL = 1.0 (subject to critical-infrastructure compliance requirements with mandatory audit reporting).

The cybersecurity risk sub-score is defined as: Cybersecurity = (0.35 * N_sens + 0.30 * N_iam + 0.20 * N_enc + 0.15 * N_comp) * 100.

## _**4.2.4 Composite Score and Risk Tiers**_

The overall migration risk is calculated as a weighted composite of the three dimensional sub-scores: Composite = (0.35 * Operational) + (0.30 * Financial) + (0.35 * Cybersecurity). The weighting structure assigns equal prominence to Operational and Cybersecurity risk (35% each) and slightly lower weight to Financial risk (30%), reflecting the finding in the literature that operational failures and security misconfigurations are generally more difficult to detect and remediate than financial overruns.

The composite score maps directly to three actionable risk tiers: LOW RISK for scores from 0.0 up to but not including 40.0, indicating that the migration plan is within acceptable risk tolerance and may proceed with standard monitoring; MEDIUM RISK for scores from 40.0 up to but not including 70.0, indicating that the migration plan contains elevated risk factors requiring targeted mitigation before proceeding; and HIGH RISK for scores from 70.0 to 100.0, indicating that the migration plan presents critical risk exposures that must be substantially addressed before the migration should be authorised.

## **4.3 User Interface (UI) Design**

The frontend of CloudRA is built to reflect the Stillwater design system, a custom visual identity prioritising clean editorial layouts, readable serif typography, warm organic colour palettes, and calm micro-animations that communicate system state changes clearly without the visual clutter commonly associated with enterprise dashboard products.

## _**4.3.1 Visual Design Tokens**_

The colour palette is intentionally organic and restrained, designed to prevent the dashboard fatigue that arises from prolonged interaction with high-contrast, saturated enterprise interfaces. The main viewport background uses a warm cream tone (hexadecimal #f4ede0), dashboard cards use a brighter cream (#faf5ec), and primary typography uses a dark charcoal-ink (#2c2620). The accent colour is a warm terracotta (#b16a48) used for interactive elements, active states, and risk-elevated indicators. Safe status indicators use a muted sage-green (#5d6e5a) that communicates stability without aggressive visual emphasis.

A custom SVG fractal noise filter is applied as a fixed overlay across the entire viewport body, creating a subtle linen grain texture that softens the flat digital appearance of the interface and reinforces the editorial, print-inspired aesthetic. This texture is embedded directly in the CSS as a base64-encoded SVG data URI, ensuring zero additional network requests.

The typography strategy pairs the variable-weight serif font Fraunces (used for display titles, composite score numerals, and card headers) with the neutral sans-serif font Inter (used for form labels, body text, and data tables). This pairing follows the established typographic principle of combining a high-personality display face with a clean workhorse body font to create clear visual hierarchy and reading rhythm.

## _**4.3.2 Interactive UI Controls**_

The dashboard implements three primary interactive visual components. The first is the Dynamic Risk Alignment Orb, a breathing animation guide positioned in the bottom corner of the viewport. This component uses CSS keyframe scaling to create a continuous pulse animation whose speed and colour are dynamically modified by the frontend JavaScript based on the computed risk tier. When the risk tier is LOW, the orb displays in sage-green with a slow nine-second pulse cycle and the status text reads "STEADY - OPTIMISED". When the risk tier is MEDIUM, the orb changes to terracotta-orange with a four-second pulse cycle and the status text reads "MODERATE - CAUTION". When the risk tier is HIGH, the orb changes to terracotta-red with a rapid 1.5-second pulse cycle and the status text reads "TENSION - RISK ALERT".

The second interactive component is the HTML5 Canvas Gauge and Radar Chart pair. The composite risk gauge draws a semicircular arc on a native HTML5 Canvas 2D rendering context, with the active arc length proportional to the computed composite score and the arc colour dynamically set to sage-green (LOW), terracotta (MEDIUM), or deep terracotta (HIGH). The radar chart draws the three dimensional sub-scores (Operational, Financial, Cybersecurity) as vertices on a triangular axis system, with concentric reference rings at 25%, 50%, 75%, and 100% providing scale context. Both charts are rendered entirely using native Canvas API calls without any external charting library dependencies.

The third interactive component is the Audit History Sidebar, which provides a scrollable, searchable list of all previously saved assessment records. Each history node displays the project name, composite score badge with colour-coded risk tier, and creation timestamp. The sidebar supports instant text filtering on project names and provides controls for asynchronous record loading (clicking a history item repopulates the form and re-renders the analytics console) and soft deletion (clicking the delete icon removes the record from the database after user confirmation).

## **4.4 System Testing and Results**

Testing was conducted programmatically using the Python pytest framework (version 8.4.1), ensuring comprehensive coverage of boundary conditions, API endpoint behaviours, pricing module fallbacks, storage layer operations, and PDF report generation.

## _**4.4.1 Test Suite Structure**_

The test suite contains 54 distinct verification tests organised across five test modules. The first module, test_api.py, contains fifteen tests that validate HTTP request handling for health check endpoints, landing page HTML serving, login page rendering, session authentication with valid and invalid credentials, dashboard redirect guards for unauthenticated users, assessment creation with thesis-aligned response fields, rejection of missing fields and non-JSON request bodies, assessment listing, retrieval, soft deletion, and PDF compliance report download endpoints.

The second module, test_scoring.py, contains twenty-seven tests that validate the risk scoring engine. These include verification that low-risk parameter profiles produce scores below the 40.0 threshold, high-risk profiles produce scores above 70.0, and that the result payload includes all thesis-aligned fields (composite_score, operational_score, financial_score, cybersec_score, risk_tier, monthly_est_usd, live_price_used, and recommendations). Parametised boundary tests verify the exact inflection points of all piecewise normalisation functions: data volume at 0, 10, and 100 TB boundaries; server count at 0, 50, and 200 boundaries; migration window at 12, 24, and 48 hour boundaries; monthly cost at 2,000 and 10,000 dollar boundaries; egress volume scaling; and CapEx-OpEx delta transitions. Three additional tests verify that the engine correctly rejects negative data volumes, negative server counts, and invalid application complexity values.

The third module, test_pricing.py, contains five tests that validate the AWS Pricing API integration. These tests use Python's unittest.mock library to simulate Boto3 client responses, verifying successful EC2 pricing retrieval, correct handling of empty API responses with automatic fallback to cached pricing, and correct exception handling when the Boto3 client raises network or timeout errors.

The fourth module, test_store.py, contains five tests that exercise the database persistence layer. Three tests validate the SQLite backend: a lifecycle test covering record creation, retrieval, listing, and soft deletion; a test verifying that retrieval of non-existent records returns None; and a schema validation test that asserts the correct column names in the assessments table. Two additional tests use mocked Boto3 DynamoDB resource objects to verify the DynamoDB backend: a lifecycle test covering item put, scan, get, and delete operations with automatic float-to-Decimal conversion, and a table creation test that verifies the system correctly provisions the CloudRiskAssessments table when it does not yet exist.

The fifth module, test_report.py, contains two tests that validate the PDF compliance report generation module, verifying that the ReportLab canvas correctly produces a valid PDF byte stream for assessments both with and without mitigation recommendations.

## _**4.4.2 Test Verification Results**_

Execution of the complete test suite returned 54 passed tests with zero failures across all five modules. The total execution time was 16.05 seconds on a Windows 11 development environment running Python 3.12.6. Three deprecation warnings were raised by the Boto3 authentication module regarding the use of datetime.datetime.utcnow(), which is scheduled for removal in a future Python version; these warnings do not affect test correctness or system functionality and originate from the third-party Boto3 library rather than the application code.

|||
|---|---|
|**Test Module**|**Tests Passed**|
|||
|test_api.py|15 of 15|
|||
|test_scoring.py|27 of 27|
|||
|test_pricing.py|5 of 5|
|||
|test_store.py|5 of 5|
|||
|test_report.py|2 of 2|
|||
|**Total**|**54 of 54 (100%)**|

**Table 4.1: Test Suite Execution Summary**

## **4.5 System Documentation**

## _**4.5.1 Environment Requirements**_

The CloudRA system requires Python version 3.12 or later. All dependency libraries are specified in the requirements.txt file located in the project root directory. The principal dependencies are Flask (web application framework), Flask-CORS (Cross-Origin Resource Sharing middleware), Boto3 (AWS SDK for Python), urllib3 (HTTP client library), and ReportLab (PDF document generation library). The pytest framework and its associated plugins are required for executing the automated test suite.

## _**4.5.2 Installation and Execution Guide**_

To initialise the development environment, the developer creates a Python virtual environment using the command "python -m venv .venv" and activates it using the platform-appropriate activation script. On Windows, the activation command is ".venv\Scriptsctivate". All dependency packages are then installed using "pip install -r requirements.txt".

To enable live queries to the AWS Pricing and DynamoDB services, the developer must configure AWS credentials by running "aws configure" and providing a valid Access Key ID, Secret Access Key, and default region (us-east-1 is recommended for Pricing API access). If AWS credentials are not configured, the system operates in fully offline mode using cached pricing data and local SQLite storage, with no degradation in functionality other than the pricing status badge displaying "Cache (Offline)" instead of "Live".

The Flask development server is launched by executing "python -m src.cloud_risk.api" from the project root directory, or alternatively by double-clicking the provided start.bat script on Windows systems. The application serves the public landing page at http://127.0.0.1:5000 and requires authentication with the administrator credentials (username: admin, password: admin) to access the assessment dashboard at the /dashboard route.

To switch the persistence backend from local SQLite to AWS DynamoDB, the developer sets the environment variable USE_DYNAMODB to true before launching the server. The system will automatically provision the CloudRiskAssessments table in the configured AWS region if it does not already exist.

To generate a completely client-side, zero-server presentation version of the framework suitable for GitHub Pages deployment, the developer executes "python build_static.py" from the project root directory. This script compiles all frontend assets into a self-contained /docs directory with relative path references, client-side authentication handling, and an embedded JavaScript scoring engine that replicates the Python backend's mathematical logic entirely in the browser.


## **CHAPTER FIVE**

## **CONCLUSION AND RECOMMENDATION**

## **5.0 Introduction**

This chapter summarizes the findings and outcomes derived from the development and deployment of the CloudRA framework. It presents the final research conclusions, details targeted recommendations for future development and academic investigation, and highlights the study's overall contributions to the computer science and IT governance domains.

## **5.1 Summary of Findings**

The development and evaluation of the CloudRA system yielded several critical findings relevant to IT project management and cloud governance practice. 

The first and most significant finding is the demonstrable reduction of subjective bias in cloud migration risk assessment. Traditional spreadsheet-based risk registers rely on qualitative, subjective ratings (typically expressed as High, Medium, or Low) that vary significantly between assessors and are influenced by individual experience, cognitive biases, and organisational pressures. The piecewise normalisation algorithms implemented in CloudRA eliminate this variability entirely; identical configuration inputs will always produce mathematically identical risk sub-scores, regardless of who conducts the assessment or when it is performed. This deterministic behaviour transforms risk assessment from a subjective exercise into a repeatable, auditable, data-driven process.

The second finding relates to FinOps alignment and financial risk mitigation. The integration of the live AWS Pricing API, with automatic timeout-based fallback to cached pricing data, successfully addresses the cloud bill shock phenomenon identified in the literature review. By linking physical infrastructure scaling metrics (server count, instance type, target region) directly to real-time monetary costs, the system enables organisations to evaluate the Operational Expenditure implications of their proposed cloud deployment before any resources are provisioned. The financial risk sub-score quantifies the gap between projected cloud costs and existing on-premises capital expenditure baselines, providing finance teams and executive leadership with a clear, numerically grounded assessment of budget exposure.

The third finding relates to security posture enforcement through quantified assessment. The cybersecurity scoring dimension highlights the critical nature of IAM permissiveness and encryption posture configurations, two areas that the Cloud Security Alliance (2022) and the Verizon Data Breach Investigations Report (2023) consistently identify as the leading causes of cloud security incidents. The scoring engine translates these technical configurations into prioritised, plain-language mitigation recommendations, bridging the communication gap between development teams who configure cloud resources and IT audit stakeholders who must assess compliance.

## **5.2 Conclusion**

This research has successfully designed, developed, and evaluated a web-based Cloud Migration Risk Assessment framework that addresses the critical gap identified in the problem statement: the absence of an automated, data-driven tool capable of dynamically assessing cloud migration risk across operational, financial, and cybersecurity dimensions simultaneously and translating that assessment into a quantified, actionable risk score supported by specific mitigation recommendations.

The CloudRA system resolves the structural limitations of manual risk registers by automating multi-dimensional risk assessment in real time, incorporating live cloud pricing data, and generating compliance-grade PDF audit reports. Through its hybrid persistence layer supporting both local SQLite operations for offline resilience and AWS DynamoDB for production-grade cloud storage, the system demonstrates a practical, cloud-native architecture suitable for both academic demonstration and enterprise deployment. The Stillwater editorial design system applied to the frontend dashboard demonstrates that enterprise audit tools can be visually engaging and ergonomically considered without sacrificing mathematical depth or professional credibility.

The system's comprehensive test suite of 54 automated tests, achieving 100% pass rates across all modules, provides confidence in the correctness of the scoring engine, the reliability of the API layer, the integrity of the persistence operations, and the validity of the generated compliance reports.

## **5.3 Recommendations**

To expand the utility of the CloudRA framework and address limitations identified during development, the following future developments are recommended.

Predictive Machine Learning Integration: The current system provides point-in-time risk assessment based on user-submitted parameters. Future iterations should integrate regression modelling capabilities to predict future cloud billing trajectories and resource utilisation trends based on historical assessment data stored in the DynamoDB audit trail. This would enable organisations to conduct trend-based forecasting in addition to snapshot risk evaluation.

Automated Infrastructure Discovery: The current system requires users to manually input infrastructure parameters such as server count, data volume, and application complexity. Future development should implement automated discovery agents that scan corporate network landscapes using cloud provider APIs and on-premises monitoring tools to automatically populate migration parameters, reducing manual configuration effort and minimising the risk of input errors.

AWS Organisations Governance Integration: The cybersecurity scoring dimension currently relies on user-reported IAM and encryption configurations. Future iterations should integrate directly with AWS Organisations APIs to dynamically inspect actual IAM policy boundaries, Service Control Policy (SCP) configurations, and encryption settings, comparing user-reported configurations against the actual state of the cloud environment and flagging discrepancies.

Multi-Cloud Provider Support: The current implementation is designed specifically for AWS migration assessments. Future development should extend the pricing integration layer to support Microsoft Azure and Google Cloud Platform, enabling organisations to conduct comparative risk assessments across multiple cloud providers and make informed multi-cloud architecture decisions.

## **5.4 Contribution to Knowledge**

This research contributes to the field of Computer Science and IT governance in the following ways.

Quantification Framework: The study establishes a formal, weighted piecewise normalisation methodology that models operational, financial, and cybersecurity risks under a single composite risk index. The mathematical specification of fourteen input parameters, their normalisation functions, dimensional weighting structures, and composite aggregation formula provides a reproducible, transparent risk quantification model that can be adopted, validated, and extended by other researchers and practitioners.

Polymorphic Database Pattern: The implementation demonstrates a reliable database design pattern that switches dynamically between local SQLite storage and cloud-hosted AWS DynamoDB tables at runtime based on environment configuration. This pattern shows how cloud-scale database systems can retain high offline resilience, making them suitable for deployment contexts where continuous internet connectivity cannot be guaranteed, such as field assessments, academic demonstrations, and air-gapped compliance environments.

Auditable Artifact Generation: The system bridges the gap between developer operations and regulatory audit processes by automating the generation of compliance-grade PDF documents compiled directly from technical configuration payloads. Each generated report contains the complete assessment input parameters, computed dimensional and composite scores, risk tier classification, and prioritised mitigation recommendations, providing a self-contained audit artifact that satisfies the documentation requirements of regulatory frameworks such as ISO 31000 and NIST SP 800-30.

