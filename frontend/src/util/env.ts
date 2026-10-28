export default function getEnvVar(name: string): string {
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-ignore
  if (window?.__env__?.[name]) {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    return window?.__env__?.[name];
  } else if (import.meta.env[name]) {
    return import.meta.env[name];
  } else {
    throw new Error(`Environment variable ${name} is not defined.`);
  }
}
