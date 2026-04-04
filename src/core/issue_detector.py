"""SEO issue detection and reporting"""
import threading
from fnmatch import fnmatch
from urllib.parse import urlparse
from difflib import SequenceMatcher


class IssueDetector:
    """Detects SEO and technical issues in crawled pages"""

    def __init__(self, exclusion_patterns=None):
        self.exclusion_patterns = exclusion_patterns or []
        self.detected_issues = []
        self.issues_lock = threading.Lock()

    def detect_issues(self, result):
        """Detect SEO issues for a crawled URL"""
        url = result.get('url', '')
        issues = []

        # Skip if URL matches exclusion patterns
        if self._should_exclude(url):
            return

        # Critical SEO Issues
        self._check_title_issues(result, issues)
        self._check_meta_description_issues(result, issues)
        self._check_heading_issues(result, issues)
        self._check_content_issues(result, issues)
        self._check_technical_issues(result, issues)
        self._check_mobile_issues(result, issues)
        self._check_accessibility_issues(result, issues)
        self._check_social_media_issues(result, issues)
        self._check_structured_data_issues(result, issues)
        self._check_performance_issues(result, issues)
        self._check_indexability_issues(result, issues)

        # Add all detected issues
        with self.issues_lock:
            self.detected_issues.extend(issues)

    def _check_title_issues(self, result, issues):
        """Check for title-related issues"""
        url = result.get('url', '')
        title = result.get('title', '')

        if not title:
            issues.append({
                'url': url,
                'type': 'error',
                'category': 'SEO',
                'issue': 'Falta etiqueta Title',
                'details': 'La página no tiene etiqueta title'
            })
        elif len(title) > 60:
            issues.append({
                'url': url,
                'type': 'warning',
                'category': 'SEO',
                'issue': 'Título demasiado largo',
                'details': f"El título tiene {len(title)} caracteres (recomendado: ≤60)"
            })
        elif len(title) < 30:
            issues.append({
                'url': url,
                'type': 'warning',
                'category': 'SEO',
                'issue': 'Título demasiado corto',
                'details': f"El título tiene {len(title)} caracteres (recomendado: 30-60)"
            })

    def _check_meta_description_issues(self, result, issues):
        """Check for meta description issues"""
        url = result.get('url', '')
        meta_desc = result.get('meta_description', '')

        if not meta_desc:
            issues.append({
                'url': url,
                'type': 'error',
                'category': 'SEO',
                'issue': 'Falta meta descripción',
                'details': 'La página no tiene meta descripción'
            })
        elif len(meta_desc) > 160:
            issues.append({
                'url': url,
                'type': 'warning',
                'category': 'SEO',
                'issue': 'Meta descripción demasiado larga',
                'details': f"La descripción tiene {len(meta_desc)} caracteres (recomendado: ≤160)"
            })
        elif len(meta_desc) < 120:
            issues.append({
                'url': url,
                'type': 'warning',
                'category': 'SEO',
                'issue': 'Meta descripción demasiado corta',
                'details': f"La descripción tiene {len(meta_desc)} caracteres (recomendado: 120-160)"
            })

    def _check_heading_issues(self, result, issues):
        """Check for heading-related issues"""
        url = result.get('url', '')

        if not result.get('h1'):
            issues.append({
                'url': url,
                'type': 'error',
                'category': 'SEO',
                'issue': 'Falta etiqueta H1',
                'details': 'La página no tiene encabezado H1'
            })

    def _check_content_issues(self, result, issues):
        """Check for content-related issues"""
        url = result.get('url', '')
        word_count = result.get('word_count', 0)

        if word_count < 300:
            issues.append({
                'url': url,
                'type': 'warning',
                'category': 'Contenido',
                'issue': 'Contenido escaso',
                'details': f'La página tiene solo {word_count} palabras (recomendado: ≥300)'
            })

    def _check_technical_issues(self, result, issues):
        """Check for technical SEO issues"""
        url = result.get('url', '')
        status_code = result.get('status_code', 0)

        if status_code >= 400 and status_code < 500:
            issues.append({
                'url': url,
                'type': 'error',
                'category': 'Técnico',
                'issue': f'{status_code} Error de cliente',
                'details': self._get_status_code_message(status_code)
            })
        elif status_code >= 500:
            issues.append({
                'url': url,
                'type': 'error',
                'category': 'Técnico',
                'issue': f'{status_code} Error de servidor',
                'details': self._get_status_code_message(status_code)
            })
        elif status_code >= 300 and status_code < 400:
            issues.append({
                'url': url,
                'type': 'info',
                'category': 'Técnico',
                'issue': f'{status_code} Redirección',
                'details': 'La URL redirige a otra ubicación'
            })

        # Canonical URL checks
        canonical_url = result.get('canonical_url', '')
        if not canonical_url:
            issues.append({
                'url': url,
                'type': 'warning',
                'category': 'Técnico',
                'issue': 'Falta URL canónica',
                'details': 'La página no tiene URL canónica especificada'
            })
        elif canonical_url != url:
            issues.append({
                'url': url,
                'type': 'warning',
                'category': 'Técnico',
                'issue': 'URL canónica diferente',
                'details': f"La URL canónica apunta a: {canonical_url}"
            })

    def _check_mobile_issues(self, result, issues):
        """Check for mobile optimization issues"""
        url = result.get('url', '')

        if not result.get('viewport'):
            issues.append({
                'url': url,
                'type': 'error',
                'category': 'Móvil',
                'issue': 'Falta etiqueta viewport',
                'details': 'La página no está optimizada para móviles'
            })

    def _check_accessibility_issues(self, result, issues):
        """Check for accessibility issues"""
        url = result.get('url', '')

        if not result.get('lang'):
            issues.append({
                'url': url,
                'type': 'warning',
                'category': 'Accesibilidad',
                'issue': 'Falta atributo de idioma',
                'details': 'La etiqueta HTML no tiene atributo lang'
            })

        # Image alt text
        images = result.get('images', [])
        images_without_alt = [img for img in images if not img.get('alt')]
        if images_without_alt:
            issues.append({
                'url': url,
                'type': 'warning',
                'category': 'Accesibilidad',
                'issue': 'Imágenes sin texto alt',
                'details': f'{len(images_without_alt)} de {len(images)} imágenes carecen de texto alternativo'
            })

    def _check_social_media_issues(self, result, issues):
        """Check for social media optimization issues"""
        url = result.get('url', '')

        if not result.get('og_tags'):
            issues.append({
                'url': url,
                'type': 'warning',
                'category': 'Social',
                'issue': 'Faltan etiquetas OpenGraph',
                'details': 'La página no tiene etiquetas OpenGraph para compartir en redes'
            })

        if not result.get('twitter_tags'):
            issues.append({
                'url': url,
                'type': 'warning',
                'category': 'Social',
                'issue': 'Faltan etiquetas Twitter Card',
                'details': 'La página no tiene etiquetas Twitter Card'
            })

    def _check_structured_data_issues(self, result, issues):
        """Check for structured data issues"""
        url = result.get('url', '')

        if not result.get('json_ld') and not result.get('schema_org'):
            issues.append({
                'url': url,
                'type': 'error',
                'category': 'Datos estructurados',
                'issue': 'Sin datos estructurados',
                'details': 'La página no tiene marcado JSON-LD ni Schema.org'
            })

    def _check_performance_issues(self, result, issues):
        """Check for performance issues"""
        url = result.get('url', '')
        response_time = result.get('response_time', 0)
        page_size = result.get('size', 0)

        if response_time > 3000:
            issues.append({
                'url': url,
                'type': 'error',
                'category': 'Rendimiento',
                'issue': 'Tiempo de respuesta lento',
                'details': f'La página tardó {response_time}ms en responder (recomendado: <3000ms)'
            })
        elif response_time > 1000:
            issues.append({
                'url': url,
                'type': 'warning',
                'category': 'Rendimiento',
                'issue': 'Tiempo de respuesta moderado',
                'details': f'La página tardó {response_time}ms en responder (recomendado: <1000ms)'
            })

        if page_size > 3 * 1024 * 1024:
            issues.append({
                'url': url,
                'type': 'error',
                'category': 'Rendimiento',
                'issue': 'Tamaño de página grande',
                'details': f'El tamaño de página es {page_size / 1024 / 1024:.1f}MB (recomendado: <3MB)'
            })
        elif page_size > 1 * 1024 * 1024:
            issues.append({
                'url': url,
                'type': 'warning',
                'category': 'Rendimiento',
                'issue': 'Tamaño de página moderado',
                'details': f'El tamaño de página es {page_size / 1024 / 1024:.1f}MB (recomendado: <1MB)'
            })

    def _check_indexability_issues(self, result, issues):
        """Check for indexability issues"""
        url = result.get('url', '')
        robots = result.get('robots', '').lower()

        if 'noindex' in robots:
            issues.append({
                'url': url,
                'type': 'error',
                'category': 'Indexabilidad',
                'issue': 'Etiqueta noindex presente',
                'details': 'La página está BLOQUEADA de los motores de búsqueda - tiene directiva noindex'
            })

        if 'nofollow' in robots:
            issues.append({
                'url': url,
                'type': 'error',
                'category': 'Indexabilidad',
                'issue': 'Etiqueta nofollow presente',
                'details': 'Los enlaces de esta página NO son seguidos por los motores de búsqueda - tiene directiva nofollow'
            })

    def detect_duplication_issues(self, all_results, similarity_threshold=0.85):
        """
        Detect content duplication across all crawled pages.

        Args:
            all_results: List of all crawled result dictionaries
            similarity_threshold: Minimum similarity ratio to flag as duplicate (0.0-1.0)
        """
        issues = []
        processed_pairs = set()

        # Compare each result with all others
        for i, result1 in enumerate(all_results):
            url1 = result1.get('url', '')

            # Skip if URL should be excluded
            if self._should_exclude(url1):
                continue

            for j, result2 in enumerate(all_results):
                # Skip same URL or already processed pairs
                if i >= j:
                    continue

                url2 = result2.get('url', '')

                # Skip if URL should be excluded
                if self._should_exclude(url2):
                    continue

                # Create unique pair identifier
                pair_key = tuple(sorted([url1, url2]))
                if pair_key in processed_pairs:
                    continue

                processed_pairs.add(pair_key)

                # Calculate similarity
                similarity = self._calculate_content_similarity(result1, result2)

                # Flag as duplicate if above threshold
                if similarity >= similarity_threshold:
                    # Add issue for both URLs
                    issues.append({
                        'url': url1,
                        'type': 'warning',
                        'category': 'Duplicación',
                        'issue': 'Contenido duplicado detectado',
                        'details': f'El contenido es {similarity*100:.1f}% similar a {url2}'
                    })
                    issues.append({
                        'url': url2,
                        'type': 'warning',
                        'category': 'Duplicación',
                        'issue': 'Contenido duplicado detectado',
                        'details': f'El contenido es {similarity*100:.1f}% similar a {url1}'
                    })

        # Add all detected duplication issues
        with self.issues_lock:
            self.detected_issues.extend(issues)

    def _calculate_content_similarity(self, result1, result2):
        """
        Calculate similarity between two page results.

        Compares title, meta description, h1, and content length.
        Returns a similarity ratio between 0.0 and 1.0.
        """
        # Extract content fields
        title1 = result1.get('title', '').lower().strip()
        title2 = result2.get('title', '').lower().strip()

        desc1 = result1.get('meta_description', '').lower().strip()
        desc2 = result2.get('meta_description', '').lower().strip()

        h1_1 = result1.get('h1', '').lower().strip()
        h1_2 = result2.get('h1', '').lower().strip()

        word_count1 = result1.get('word_count', 0)
        word_count2 = result2.get('word_count', 0)

        # Calculate individual similarities
        title_sim = self._text_similarity(title1, title2) if title1 and title2 else 0
        desc_sim = self._text_similarity(desc1, desc2) if desc1 and desc2 else 0
        h1_sim = self._text_similarity(h1_1, h1_2) if h1_1 and h1_2 else 0

        # Word count similarity (1.0 if within 10% of each other)
        if word_count1 and word_count2:
            max_count = max(word_count1, word_count2)
            min_count = min(word_count1, word_count2)
            word_count_sim = min_count / max_count if max_count > 0 else 0
        else:
            word_count_sim = 0

        # Weighted average (title and description are most important)
        weights = {
            'title': 0.35,
            'desc': 0.35,
            'h1': 0.20,
            'word_count': 0.10
        }

        overall_similarity = (
            title_sim * weights['title'] +
            desc_sim * weights['desc'] +
            h1_sim * weights['h1'] +
            word_count_sim * weights['word_count']
        )

        return overall_similarity

    def _text_similarity(self, text1, text2):
        """Calculate similarity ratio between two text strings using SequenceMatcher"""
        if not text1 or not text2:
            return 0.0
        return SequenceMatcher(None, text1, text2).ratio()

    def _should_exclude(self, url):
        """Check if URL should be excluded from issue detection"""
        parsed = urlparse(url)
        path = parsed.path

        for pattern in self.exclusion_patterns:
            if '*' in pattern:
                if fnmatch(path, pattern):
                    return True
            elif path == pattern or path.startswith(pattern.rstrip('*')):
                return True

        return False

    def _get_status_code_message(self, status_code):
        """Get descriptive message for HTTP status codes"""
        messages = {
            400: 'Solicitud incorrecta',
            401: 'No autorizado',
            403: 'Prohibido',
            404: 'No encontrado',
            405: 'Método no permitido',
            406: 'No aceptable',
            408: 'Tiempo de espera agotado',
            410: 'Recurso eliminado',
            429: 'Demasiadas solicitudes',
            500: 'Error interno del servidor',
            501: 'No implementado',
            502: 'Puerta de enlace incorrecta',
            503: 'Servicio no disponible',
            504: 'Tiempo de espera de puerta de enlace',
            505: 'Versión HTTP no soportada'
        }
        return messages.get(status_code, f'Error HTTP {status_code}')

    def get_issues(self):
        """Get all detected issues"""
        with self.issues_lock:
            return self.detected_issues.copy()

    def reset(self):
        """Reset detected issues"""
        with self.issues_lock:
            self.detected_issues.clear()
