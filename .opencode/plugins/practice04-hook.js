// practice04-hook: auto-run practice_04 runner after edits in project/
// Saved in UTF-8. Keeps messages ASCII-only to avoid mojibake.

import { exec } from "node:child_process"
import { appendFileSync, mkdirSync } from "node:fs"
import { join } from "node:path"

/**
 * Parse file paths from apply_patch-like patch text. Looks for lines:
 *   *** Add File: path
 *   *** Update File: path
 *   *** Delete File: path
 */
function parsePathsFromPatch(patchText) {
  if (typeof patchText !== "string") return []
  const paths = []
  const re = /^\*\*\*\s+(?:Add|Update|Delete)\s+File:\s+(.+)$/gm
  let m
  while ((m = re.exec(patchText)) !== null) {
    paths.push(m[1].trim())
  }
  return paths
}

function writeLog(directory, msg) {
  try {
    const logDir = join(directory, "practices", "practice_04", "logs")
    mkdirSync(logDir, { recursive: true })
    const line = `${new Date().toISOString()} practice04-hook ${msg}\n`
    appendFileSync(join(logDir, "hook.log"), line, { encoding: "utf8" })
  } catch {
    // best-effort logging only
  }
}

export default async function practice04Hook({ directory }) {
  // directory is the workspace root the user opened
  return {
    async "tool.execute.after"(input, output) {
      try {
        const name = input?.name || input?.tool || input?.toolName || ""
        if (!name) return

        // Only react to edits via apply_patch/edit tool
        const isEdit = name === "apply_patch" || name === "edit"
        if (!isEdit) return

        const patchText = input?.patchText || input?.args?.patchText || ""
        const paths = parsePathsFromPatch(patchText)
        const touchedProject = paths.some((p) =>
          p.replace(/\\/g, "/").startsWith("practices/practice_04/project/")
        )
        if (!touchedProject) return

        writeLog(directory, `detected edit; tool=${name}; files=${paths.join(",")}`)

        // Kick runner. Use Node child_process to avoid depending on client internals.
        const cmd = `python practices/practice_04/runner/run_tests.py`
        exec(cmd, { cwd: directory }, (err, stdout, stderr) => {
          const status = err ? `error: ${err.message}` : "ok"
          writeLog(directory, `runner ${status}`)
          if (stdout) writeLog(directory, `stdout: ${stdout.trim()}`)
          if (stderr) writeLog(directory, `stderr: ${stderr.trim()}`)
        })
      } catch (e) {
        writeLog(directory, `hook error: ${e?.message || String(e)}`)
      }
    },
  }
}

// Also allow named export form for compatibility
export const plugin = practice04Hook
