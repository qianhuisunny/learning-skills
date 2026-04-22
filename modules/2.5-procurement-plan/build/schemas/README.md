# SCORM 1.2 XSD schemas

**Status: deferred for MVP.** SCORM Cloud does not require the XSD files to be shipped inside the package. The `schemaLocation` attribute in `imsmanifest.xml` is informational — SCORM Cloud uses its own validation. If a future LMS strictly enforces the schemas, drop the 4 XSD files here:

- `adlcp_rootv1p2.xsd` (ADL CP extensions)
- `ims_xml.xsd` (IMS XML base)
- `imscp_rootv1p1p2.xsd` (IMS Content Packaging root)
- `imsmd_rootv1p2p1.xsd` (IMS Metadata root)

Source: ADL's SCORM 1.2 conformance kit (public domain). The ADL site is offline; a working mirror has not been located as of 2026-04-10. If you need them, extract from any real SCORM 1.2 sample package (e.g., Rustici's "Golf Example" or any course authored in Articulate/Captivate/iSpring).

`pack_scorm.py` currently copies `shell/schemas/` wholesale into `build/schemas/`, so dropping the XSDs here later will auto-ship them with future builds.
