const PptxGenJS = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "OpenAI Codex";
pptx.company = "University of Washington Bothell";
pptx.subject = "HuskyAdvisor weekly status update";
pptx.title = "HuskyAdvisor Status Update";
pptx.lang = "en-US";
pptx.theme = {
  headFontFace: "Arial",
  bodyFontFace: "Arial",
  lang: "en-US",
};

const C = {
  purple: "32067D",
  gold: "F3C300",
  white: "FFFFFF",
  black: "1C1C1C",
  light: "F7F7FB",
  border: "5A4B82",
  red: "C92B2B",
  green: "1F7A38",
  beige: "FFF0C9",
  gray: "666666",
};

function addHeader(slide, title) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 13.333,
    h: 0.95,
    fill: { color: C.purple },
    line: { color: C.purple },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0.95,
    w: 13.333,
    h: 0.06,
    fill: { color: C.gold },
    line: { color: C.gold },
  });
  slide.addText(title, {
    x: 0.4,
    y: 0.22,
    w: 12.5,
    h: 0.35,
    fontFace: "Arial",
    fontSize: 25,
    bold: true,
    color: C.white,
    align: "center",
  });
}

function addPanel(slide, opts) {
  slide.addShape(pptx.ShapeType.rect, {
    x: opts.x,
    y: opts.y,
    w: opts.w,
    h: opts.h,
    fill: { color: opts.fill || C.white },
    line: { color: opts.line || C.border, pt: 1.25 },
  });
  if (opts.header) {
    slide.addShape(pptx.ShapeType.rect, {
      x: opts.x,
      y: opts.y,
      w: opts.w,
      h: opts.headerH || 0.42,
      fill: { color: opts.headerColor || C.purple },
      line: { color: opts.headerColor || C.purple, pt: 1 },
    });
    slide.addText(opts.header, {
      x: opts.x + 0.1,
      y: opts.y + 0.09,
      w: opts.w - 0.2,
      h: 0.2,
      fontSize: 17,
      bold: true,
      color: C.white,
      align: "center",
    });
  }
}

function addBullets(slide, bullets, box, fontSize = 18) {
  const text = bullets.map((bullet) => `• ${bullet}`).join("\n\n");
  slide.addText(text, {
    x: box.x,
    y: box.y,
    w: box.w,
    h: box.h,
    fontFace: "Arial",
    fontSize,
    color: C.black,
    breakLine: false,
    margin: 0.08,
    fit: "shrink",
    valign: "top",
  });
}

function addMetricCard(slide, x, y, w, h, title, value, subtitle) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h,
    rectRadius: 0.03,
    fill: { color: C.light },
    line: { color: C.border, pt: 1.2 },
  });
  slide.addText(title, {
    x: x + 0.08,
    y: y + 0.08,
    w: w - 0.16,
    h: 0.2,
    fontFace: "Arial",
    fontSize: 12,
    color: C.gray,
    bold: true,
    align: "center",
  });
  slide.addText(value, {
    x: x + 0.08,
    y: y + 0.26,
    w: w - 0.16,
    h: 0.32,
    fontFace: "Arial",
    fontSize: 24,
    bold: true,
    color: C.purple,
    align: "center",
  });
  slide.addText(subtitle, {
    x: x + 0.08,
    y: y + 0.57,
    w: w - 0.16,
    h: 0.18,
    fontFace: "Arial",
    fontSize: 9.5,
    color: C.gray,
    align: "center",
  });
}

// Slide 1
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 13.333,
    h: 4.1,
    fill: { color: C.purple },
    line: { color: C.purple },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 4.1,
    w: 13.333,
    h: 0.08,
    fill: { color: C.gold },
    line: { color: C.gold },
  });
  slide.addText("HuskyAdvisor", {
    x: 1.2,
    y: 1.35,
    w: 10.9,
    h: 0.6,
    fontFace: "Arial",
    fontSize: 26,
    bold: true,
    color: C.white,
    align: "center",
  });
  slide.addText("DYOP Final Project | University of Washington Bothell", {
    x: 1.6,
    y: 2.2,
    w: 10.1,
    h: 0.25,
    fontSize: 16,
    color: "F7D84D",
    align: "center",
  });
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 4.75,
    y: 2.72,
    w: 3.8,
    h: 0.56,
    rectRadius: 0.04,
    fill: { color: C.gold },
    line: { color: C.gold },
  });
  slide.addText("May 26, 2026 Status Update", {
    x: 4.85,
    y: 2.88,
    w: 3.6,
    h: 0.18,
    fontSize: 16,
    bold: true,
    color: C.purple,
    align: "center",
  });
  addPanel(slide, { x: 2.0, y: 4.65, w: 9.3, h: 1.6, fill: C.white });
  slide.addText("Team Members", {
    x: 2.3,
    y: 5.0,
    w: 8.7,
    h: 0.25,
    fontSize: 20,
    color: C.black,
    bold: false,
    align: "center",
  });
  slide.addText("Matiyas Dawit   |   Christie Yiu   |   Leslie Yiu", {
    x: 2.25,
    y: 5.45,
    w: 8.8,
    h: 0.3,
    fontSize: 18,
    color: C.black,
    align: "center",
  });
  slide.addText("CSS 382", {
    x: 5.75,
    y: 6.03,
    w: 1.8,
    h: 0.2,
    fontSize: 12,
    color: C.gray,
    align: "center",
  });
}

// Slide 2
{
  const slide = pptx.addSlide();
  addHeader(slide, "This Week: Planned vs. Done");
  addPanel(slide, { x: 0.85, y: 1.25, w: 5.0, h: 4.8, header: "Planned" });
  addPanel(slide, { x: 7.45, y: 1.25, w: 5.0, h: 4.8, header: "Done" });
  addBullets(slide, [
    "Expand UW Bothell major and course coverage beyond the original sample set.",
    "Improve recommendation quality so the system stops repeating taken courses and better matches goals.",
    "Strengthen company alignment, internship prep, and roadmap support for the website demo.",
  ], { x: 1.15, y: 1.9, w: 4.4, h: 3.55 }, 15.5);
  addBullets(slide, [
    "Expanded support to 6 UW Bothell-relevant majors and organized 122 course records by pathway.",
    "Added 120 company targets with company-aware course mappings and better internship / roadmap matching.",
    "Ran regression tests and a 58-profile stress simulation to verify stronger, less redundant recommendations.",
  ], { x: 7.75, y: 1.9, w: 4.4, h: 3.55 }, 15.5);
  slide.addText("Tip: we used this week to move HuskyAdvisor from a small prototype toward a more believable advising system.", {
    x: 1.0,
    y: 6.1,
    w: 11.2,
    h: 0.2,
    fontSize: 10.5,
    color: C.gray,
    italic: true,
    align: "center",
  });
}

// Slide 3
{
  const slide = pptx.addSlide();
  addHeader(slide, "Progress / Demo");
  addPanel(slide, { x: 0.75, y: 1.2, w: 6.3, h: 4.7, fill: "FBFBFE" });
  slide.addText("System pipeline now working locally:", {
    x: 1.0, y: 1.5, w: 5.0, h: 0.3, fontFace: "Arial", fontSize: 18, bold: true, color: C.black,
  });
  addBullets(slide, [
    "React website collects student major, standing, completed courses, goals, and target company.",
    "FastAPI backend receives the profile and calls the advising engine.",
    "The engine returns course recommendations, company alignment, internship-prep guidance, and roadmap output.",
    "Out-of-scope profiles now get honest warnings instead of fake recommendations.",
  ], { x: 1.0, y: 1.95, w: 5.7, h: 3.35 }, 14.5);
  slide.addText("Demo highlights", {
    x: 7.55, y: 1.35, w: 4.2, h: 0.25, fontFace: "Arial", fontSize: 18, bold: true, color: C.black, align: "center",
  });
  addMetricCard(slide, 7.45, 1.8, 2.2, 0.95, "Supported majors", "6", "CSSE, AC, EE, CompE, Data Viz, Business");
  addMetricCard(slide, 9.95, 1.8, 2.2, 0.95, "Courses", "122", "organized across major pathways");
  addMetricCard(slide, 7.45, 2.95, 2.2, 0.95, "Companies", "120", "company-aware mappings added");
  addMetricCard(slide, 9.95, 2.95, 2.2, 0.95, "Stress tests", "58", "simulated student profiles");
  addMetricCard(slide, 8.7, 4.1, 2.2, 0.95, "Regression tests", "13", "passing in current backend");
  slide.addText("Concrete metric: 13 regression tests passing and 58 simulated profiles rated strong in the latest stress-test pass.", {
    x: 7.4,
    y: 5.35,
    w: 4.8,
    h: 0.45,
    fontFace: "Arial",
    fontSize: 12,
    color: C.gray,
    align: "center",
  });
}

// Slide 4
{
  const slide = pptx.addSlide();
  addHeader(slide, "Blockers & Next Week's Plan");
  addPanel(slide, { x: 0.9, y: 1.2, w: 4.95, h: 3.1, header: "Blockers / Risks", headerColor: C.red });
  addPanel(slide, { x: 7.45, y: 1.2, w: 4.95, h: 4.25, header: "Next Week's Goals", headerColor: C.green });
  addBullets(slide, [
    "Newer pathways like Data Visualization and Business still rely on some shared CSS/BIS courses more than deep major-specific catalogs.",
    "The current demo is strongest when both the local frontend and backend are running; deployment polish is still limited.",
    "We still want clearer official source guidance for UWB degree requirements and schedule data.",
  ], { x: 1.15, y: 1.9, w: 4.45, h: 2.25 }, 14.2);
  addPanel(slide, { x: 0.9, y: 4.55, w: 4.95, h: 1.0, fill: C.beige, line: C.border });
  slide.addText("Help needed from instructor:\nGuidance on the best official UWB source for course, schedule, and degree-requirement data.", {
    x: 1.15,
    y: 4.83,
    w: 4.45,
    h: 0.44,
    fontFace: "Arial",
    fontSize: 12.5,
    color: C.black,
    align: "center",
    valign: "mid",
  });
  addBullets(slide, [
    "Deepen Data Visualization and Business Administration metadata so the newer pathways stay as strong as CSSE.",
    "Polish the frontend explanation text so users can clearly see why each recommendation was chosen.",
    "Prepare a cleaner end-to-end demo flow and verify the website/API behavior on the main sample profiles.",
    "Finalize presentation polish and team walkthrough for the final class demo.",
  ], { x: 7.75, y: 1.9, w: 4.45, h: 3.25 }, 14.2);
}

// Slide 5
{
  const slide = pptx.addSlide();
  addHeader(slide, "Individual Contributions");
  slide.addText("Student", {
    x: 0.9, y: 1.3, w: 1.5, h: 0.2, fontSize: 14, bold: true, color: C.black, align: "center",
  });
  slide.addText("Hours", {
    x: 2.45, y: 1.3, w: 1.0, h: 0.2, fontSize: 14, bold: true, color: C.black, align: "center",
  });
  slide.addText("What I Worked On This Week", {
    x: 3.7, y: 1.3, w: 8.6, h: 0.2, fontSize: 14, bold: true, color: C.black, align: "center",
  });

  const rows = [
    {
      y: 1.55,
      name: "Matiyas Dawit",
      hours: "1.5 hrs",
      work: "Expanded majors, course coverage, and company mappings; improved recommendation realism, testing, and project documentation.",
    },
    {
      y: 2.45,
      name: "Christie Yiu",
      hours: "TBD",
      work: "Frontend website work, early prototype flow, and UI / deployment support for the HuskyAdvisor experience.",
    },
    {
      y: 3.35,
      name: "Leslie Yiu",
      hours: "TBD",
      work: "Backend API and integration support so the website can call the advising engine through structured endpoints.",
    },
  ];

  rows.forEach((row) => {
    slide.addShape(pptx.ShapeType.rect, {
      x: 0.8,
      y: row.y,
      w: 11.7,
      h: 0.88,
      fill: { color: C.white },
      line: { color: C.border, pt: 1 },
    });
    slide.addText(row.name, {
      x: 0.95, y: row.y + 0.22, w: 1.4, h: 0.2, fontFace: "Arial", fontSize: 12.5, color: C.black, align: "center",
    });
    slide.addText(row.hours, {
      x: 2.45, y: row.y + 0.22, w: 1.0, h: 0.2, fontFace: "Arial", fontSize: 12.5, color: C.black, align: "center",
    });
    slide.addText(`• ${row.work}`, {
      x: 3.8, y: row.y + 0.13, w: 8.2, h: 0.55, fontFace: "Arial", fontSize: 11.8, color: C.black, fit: "shrink",
    });
  });

  slide.addShape(pptx.ShapeType.rect, {
    x: 0.8,
    y: 4.45,
    w: 11.7,
    h: 0.72,
    fill: { color: "FFF6D8" },
    line: { color: C.gold, pt: 1 },
  });
  slide.addText("Team total this week: confirm final hours with teammates before submission.", {
    x: 1.0, y: 4.67, w: 5.0, h: 0.2, fontSize: 12.5, bold: true, color: C.black,
  });
  slide.addText("Cumulative team hours to date: update after final team check-in.", {
    x: 6.1, y: 4.67, w: 5.7, h: 0.2, fontSize: 12.5, bold: true, color: C.black, align: "right",
  });
  slide.addText("Individual peer review is submitted separately and confidentially on Canvas.", {
    x: 0.9, y: 5.45, w: 11.7, h: 0.2, fontSize: 11, italic: true, color: C.gray, align: "center",
  });
}

const outDir = path.join(process.cwd(), "deliverables");
fs.mkdirSync(outDir, { recursive: true });
const outPath = path.join(outDir, "HuskyAdvisor_Status_Update_GoogleSlidesFriendly.pptx");

pptx.writeFile({ fileName: outPath }).then(() => {
  console.log(outPath);
}).catch((err) => {
  console.error(err);
  process.exit(1);
});
