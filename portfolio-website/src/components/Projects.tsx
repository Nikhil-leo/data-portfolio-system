"use client";
import { useState } from "react";
import { Github, ExternalLink, BarChart2, TrendingUp } from "lucide-react";
import projectsData from "@/data/projects.json";

type Project = typeof projectsData[number];

const ALL_TAGS = ["All", ...Array.from(new Set(projectsData.flatMap((p) => p.tags)))];

function ProjectCard({ project }: { project: Project }) {
  return (
    <div className="glass-card p-6 flex flex-col gap-4 hover:border-blue-500/50 transition-all duration-300 group">
      {/* Header */}
      <div className="flex items-start justify-between gap-2">
        <h3 className="font-bold text-lg group-hover:text-blue-400 transition-colors leading-snug">
          {project.title}
        </h3>
        {project.featured && (
          <span className="shrink-0 text-xs px-2 py-1 bg-teal-500/10 text-teal-400 border border-teal-500/20 rounded-full">
            Featured
          </span>
        )}
      </div>

      <p className="text-slate-400 text-sm leading-relaxed flex-1">
        {project.description}
      </p>

      {/* KPIs */}
      {project.kpis && project.kpis.length > 0 && (
        <div>
          <p className="text-xs text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-1">
            <TrendingUp size={12} /> KPIs
          </p>
          <div className="flex flex-wrap gap-1.5">
            {project.kpis.map((kpi) => (
              <span key={kpi} className="text-xs px-2 py-0.5 bg-teal-500/10 text-teal-300 rounded-full border border-teal-500/20">
                {kpi}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Tools */}
      <div className="flex flex-wrap gap-1.5">
        {project.tools.map((tool) => (
          <span key={tool} className="pill text-xs">{tool}</span>
        ))}
      </div>

      {/* Dashboard badges */}
      <div className="flex gap-2">
        {project.dashboards.tableau && (
          <span className="flex items-center gap-1 text-xs px-2 py-1 bg-orange-500/10 text-orange-300 border border-orange-500/20 rounded">
            <BarChart2 size={11} /> Tableau
          </span>
        )}
        {project.dashboards.powerbi && (
          <span className="flex items-center gap-1 text-xs px-2 py-1 bg-yellow-500/10 text-yellow-300 border border-yellow-500/20 rounded">
            <BarChart2 size={11} /> Power BI
          </span>
        )}
      </div>

      {/* Links */}
      <div className="flex gap-3 pt-2 border-t border-slate-700/50">
        {project.githubUrl && (
          <a href={project.githubUrl} target="_blank" rel="noreferrer"
            className="flex items-center gap-1.5 text-sm text-slate-400 hover:text-white transition-colors">
            <Github size={15} /> Code
          </a>
        )}
        {project.tableauUrl && project.tableauUrl !== "https://public.tableau.com/views/your-workbook" && (
          <a href={project.tableauUrl} target="_blank" rel="noreferrer"
            className="flex items-center gap-1.5 text-sm text-slate-400 hover:text-orange-400 transition-colors">
            <ExternalLink size={15} /> Tableau
          </a>
        )}
        {project.powerbiUrl && project.powerbiUrl !== "https://app.powerbi.com/view?r=your-report-id" && (
          <a href={project.powerbiUrl} target="_blank" rel="noreferrer"
            className="flex items-center gap-1.5 text-sm text-slate-400 hover:text-yellow-400 transition-colors">
            <ExternalLink size={15} /> Power BI
          </a>
        )}
      </div>
    </div>
  );
}

export default function Projects() {
  const [activeTag, setActiveTag] = useState("All");

  const filtered = activeTag === "All"
    ? projectsData
    : projectsData.filter((p) => p.tags.includes(activeTag));

  return (
    <section id="projects" className="py-24 max-w-6xl mx-auto px-6">
      <div className="text-center mb-12">
        <h2 className="section-title">
          My <span className="gradient-text">Projects</span>
        </h2>
        <div className="w-16 h-1 bg-gradient-to-r from-blue-500 to-teal-500 mx-auto rounded mb-6" />
        <p className="text-slate-400 max-w-xl mx-auto">
          End-to-end analytics projects — from raw data to published dashboards.
        </p>
      </div>

      {/* Tag filters */}
      <div className="flex flex-wrap justify-center gap-2 mb-10">
        {ALL_TAGS.map((tag) => (
          <button
            key={tag}
            onClick={() => setActiveTag(tag)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
              activeTag === tag
                ? "bg-blue-600 text-white"
                : "bg-slate-800 text-slate-400 hover:bg-slate-700"
            }`}
          >
            {tag}
          </button>
        ))}
      </div>

      {/* Grid */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map((project) => (
          <ProjectCard key={project.id} project={project} />
        ))}
      </div>

      {filtered.length === 0 && (
        <p className="text-center text-slate-500 py-12">No projects match this filter.</p>
      )}
    </section>
  );
}
